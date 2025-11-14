# Confluence: Feature 1 - Modular Parts Architecture

**Page Type**: Feature Documentation  
**Space**: Engineering / Robotics  
**Labels**: architecture, modular-design, python, core-feature  
**Jira Ticket**: [DONKEY-001](JIRA_TICKETS.md#story-1-modular-parts-architecture)  
**Status**: In Development  

---

## Feature Overview

### Business Logic

**Problem Statement**:
Traditional robot control systems require developers to modify core vehicle code whenever new sensors, actuators, or processing components are added. This creates several challenges:
- Tight coupling between components makes the system difficult to maintain
- Adding new hardware requires extensive code changes
- Testing individual components is difficult
- Code reusability across different robot configurations is limited

**Business Value**:
- **Faster Development**: Reduce time to integrate new components from days to hours
- **Lower Maintenance Costs**: Isolated components reduce risk of breaking existing functionality
- **Increased Flexibility**: Support multiple robot configurations with the same codebase
- **Better Testing**: Components can be tested independently
- **Community Contribution**: Easier for community members to contribute new parts

**Success Metrics**:
- Time to add a new sensor/actuator part: < 2 hours
- Zero breaking changes when adding new parts
- 100% of core parts have unit tests
- Community-contributed parts library grows by 10+ parts per quarter

---

## Technical Architecture

### System Design

The modular parts architecture is built around three core concepts:

1. **Vehicle Class**: Central orchestrator that manages all parts
2. **Memory Channels**: Shared data bus for inter-part communication
3. **Part Interface**: Standard contract that all parts must implement

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Vehicle Class                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Drive Loop (10-30 Hz)               │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │            Memory Channel System                 │  │
│  │  { 'cam/image': <image>,                        │  │
│  │    'user/angle': 0.5,                           │  │
│  │    'pilot/throttle': 0.3, ... }                 │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
         │              │              │
    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
    │  Part 1 │    │  Part 2 │    │  Part N │
    │ Camera  │    │ Actuator│    │  Pilot  │
    │         │    │         │    │         │
    │ Inputs: │    │ Inputs: │    │ Inputs: │
    │  []     │    │ ['angle']│   │ ['image']│
    │         │    │         │    │         │
    │ Outputs:│    │ Outputs:│    │ Outputs:│
    │ ['image']│   │ ['motor']│   │ ['angle']│
    └─────────┘    └─────────┘    └─────────┘
```

### Core Components

#### 1. Vehicle Class (`donkeycar/vehicle.py`)

**Responsibilities**:
- Manage lifecycle of all parts
- Execute drive loop at specified frequency
- Route data between parts via memory channels
- Handle threading for async parts
- Provide part registration API

**Key Methods**:
```python
class Vehicle:
    def __init__(self, mem=None):
        """Initialize vehicle with optional memory instance"""
        
    def add(self, part, inputs=[], outputs=[], 
            threaded=False, run_condition=None):
        """Add a part to the vehicle with input/output channels"""
        
    def start(self, rate_hz=10, max_loop_count=None):
        """Start the drive loop"""
        
    def stop(self):
        """Stop the vehicle and cleanup"""
```

**Technical Implementation**:
- Uses `Memory` class for channel storage (dictionary-based)
- Drive loop executes parts sequentially in registration order
- Threaded parts run in separate threads with `run_threaded()` method
- Run conditions allow conditional part execution

#### 2. Memory Channel System (`donkeycar/memory.py`)

**Purpose**: Provide shared data storage for inter-part communication

**Design**:
- Dictionary-based storage: `mem['channel_name'] = value`
- Type-agnostic: Can store any Python object
- Thread-safe: Uses locks for concurrent access
- Channel naming convention: `{source}/{data_type}` (e.g., `cam/image`, `user/angle`)

**Example Usage**:
```python
# Part writes to memory
self.mem['cam/image'] = image_array

# Another part reads from memory
image = self.mem['cam/image']
```

#### 3. Part Interface

**Contract**: All parts must implement at least one of:
- `run(*args)`: Synchronous execution
- `run_threaded(*args)`: Threaded execution (returns immediately)
- `update()`: Background thread function (for threaded parts)

**Part Structure**:
```python
class MyPart:
    def __init__(self):
        """Initialize part with configuration"""
        
    def run(self, input1, input2):
        """
        Synchronous execution
        Args:
            input1, input2: Values from memory channels
        Returns:
            output1, output2: Values to write to memory channels
        """
        # Process inputs
        result = process(input1, input2)
        return result
        
    def shutdown(self):
        """Cleanup resources when vehicle stops"""
```

---

## Implementation Details

### Adding a Part to Vehicle

**Process Flow**:
1. Developer creates part class
2. Instantiate part: `part = MyPart()`
3. Register with vehicle: `V.add(part, inputs=['channel1'], outputs=['channel2'])`
4. Vehicle maps inputs from memory to part's `run()` method
5. Vehicle writes part's return values to output channels

**Code Example**:
```python
import donkeycar as dk

# Initialize vehicle
V = dk.Vehicle()

# Create and add camera part
cam = dk.parts.PiCamera()
V.add(cam, outputs=['cam/image_array'], threaded=True)

# Create and add actuator part
actuator = dk.parts.PCA9685()
V.add(actuator, 
      inputs=['user/angle', 'user/throttle'],
      outputs=['motor/left', 'motor/right'])

# Start vehicle
V.start(rate_hz=20)
```

### Threaded vs Non-Threaded Parts

**Non-Threaded Parts**:
- Execute synchronously in drive loop
- Must complete quickly (< 100ms) to maintain loop frequency
- Use for: Simple transformations, calculations, data routing

**Threaded Parts**:
- Execute in separate thread
- Use `run_threaded()` which returns immediately with cached result
- Background `update()` method processes in thread
- Use for: I/O operations (camera, network), slow processing, blocking operations

**Example Threaded Part**:
```python
class SlowCamera:
    def __init__(self):
        self.current_image = None
        self.running = True
        
    def update(self):
        """Runs in background thread"""
        while self.running:
            self.current_image = self.capture_image()
            time.sleep(0.1)
            
    def run_threaded(self):
        """Called by drive loop - returns immediately"""
        return self.current_image
```

### Input/Output Channel Mapping

**Mapping Logic**:
1. Vehicle reads values from memory channels specified in `inputs`
2. Passes values as arguments to part's `run()` or `run_threaded()` method
3. Part returns values (single value or tuple)
4. Vehicle writes return values to channels specified in `outputs`

**Channel Resolution**:
- Inputs: Read from memory before part execution
- Outputs: Written to memory after part execution
- Order matters: Output order must match return value order

---

## Data Flow

### Example: Camera → Controller → Actuator

```
┌─────────────┐
│   Camera    │
│   Part      │
│             │
│ Output:     │
│ 'cam/image' │
└──────┬──────┘
       │
       │ Writes to memory
       ▼
┌─────────────────┐
│  Memory Channel │
│  'cam/image'    │
└────────┬────────┘
         │
         │ Read by controller
         ▼
┌─────────────┐
│ Controller  │
│   Part      │
│             │
│ Input:      │
│ 'cam/image' │
│             │
│ Output:     │
│ 'user/angle'│
│ 'user/throttle'│
└──────┬──────┘
       │
       │ Writes to memory
       ▼
┌─────────────────┐
│  Memory Channel │
│  'user/angle'   │
│  'user/throttle'│
└────────┬────────┘
         │
         │ Read by actuator
         ▼
┌─────────────┐
│  Actuator   │
│   Part      │
│             │
│ Input:      │
│ 'user/angle'│
│ 'user/throttle'│
│             │
│ Output:     │
│ 'motor/left'│
│ 'motor/right'│
└─────────────┘
```

---

## Technical Specifications

### Performance Requirements

- **Drive Loop Frequency**: 10-30 Hz (configurable)
- **Part Execution Time**: < 100ms for non-threaded parts
- **Memory Access**: O(1) dictionary lookup
- **Thread Overhead**: Minimal (< 1ms per threaded part)

### Memory Management

- **Channel Storage**: Dictionary with string keys
- **Data Types**: Any Python object (images, numbers, strings, objects)
- **Memory Cleanup**: Automatic garbage collection
- **Thread Safety**: Locks for concurrent access (if needed)

### Error Handling

- **Missing Channels**: Parts receive `None` if channel doesn't exist
- **Part Failures**: Exceptions logged, vehicle continues (configurable)
- **Thread Failures**: Threaded part failures don't crash drive loop
- **Validation**: Type checking for inputs/outputs (optional)

---

## Testing Strategy

### Unit Tests

**Vehicle Class**:
- Test part registration
- Test input/output channel mapping
- Test drive loop execution
- Test threading behavior
- Test error handling

**Part Interface**:
- Test synchronous execution
- Test threaded execution
- Test input/output handling
- Test shutdown behavior

### Integration Tests

- Test multiple parts working together
- Test data flow through memory channels
- Test performance under load
- Test thread synchronization

### Example Test

```python
def test_vehicle_add_part():
    V = dk.Vehicle()
    
    # Create mock part
    class TestPart:
        def run(self, x):
            return x * 2
    
    # Add part
    V.add(TestPart(), inputs=['test_input'], outputs=['test_output'])
    
    # Set input
    V.mem['test_input'] = 5
    
    # Execute one loop
    V.start(rate_hz=1, max_loop_count=1)
    
    # Verify output
    assert V.mem['test_output'] == 10
```

---

## Usage Examples

### Example 1: Adding a Camera

```python
V = dk.Vehicle()
cam = dk.parts.PiCamera(resolution=(160, 120))
V.add(cam, outputs=['cam/image_array'], threaded=True)
```

### Example 2: Adding a Custom Sensor

```python
class TemperatureSensor:
    def __init__(self):
        self.sensor = Adafruit_DHT.DHT22(4)
    
    def run(self):
        humidity, temperature = Adafruit_DHT.read_retry(
            self.sensor, 4)
        return temperature

V = dk.Vehicle()
temp_sensor = TemperatureSensor()
V.add(temp_sensor, outputs=['sensor/temperature'])
```

### Example 3: Adding a Data Logger

```python
class DataLogger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.data = []
    
    def run(self, image, angle, throttle):
        self.data.append({
            'image': image,
            'angle': angle,
            'throttle': throttle,
            'timestamp': time.time()
        })
        return image, angle, throttle  # Pass through

V = dk.Vehicle()
logger = DataLogger('log.json')
V.add(logger, 
      inputs=['cam/image', 'user/angle', 'user/throttle'],
      outputs=['cam/image', 'user/angle', 'user/throttle'])
```

---

## Dependencies

### Core Dependencies
- Python 3.5+
- No external dependencies for core architecture

### Part Dependencies
- Parts may have their own dependencies (e.g., `picamera`, `numpy`)
- Dependencies are isolated to individual parts

---

## Future Enhancements

1. **Part Versioning**: Support multiple versions of same part
2. **Part Marketplace**: Centralized repository of community parts
3. **Hot Reloading**: Add/remove parts without restarting vehicle
4. **Part Validation**: Schema validation for inputs/outputs
5. **Performance Profiling**: Built-in timing and profiling for parts
6. **Visual Part Editor**: GUI for configuring parts and connections

---

## Related Documentation

- [Main Project Documentation](CONFLUENCE_PAGE.md)
- [Parts Guide](docs/parts/about.md)
- [Vehicle API Reference](donkeycar/vehicle.py)
- [Memory System](donkeycar/memory.py)

---

**Last Updated**: [Date]  
**Page Owner**: Engineering Team  
**Review Frequency**: Quarterly

