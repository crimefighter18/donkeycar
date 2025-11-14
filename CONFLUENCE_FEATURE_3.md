# Confluence: Feature 3 - Web-Based Control and Monitoring Interface

**Page Type**: Feature Documentation  
**Space**: Engineering / Robotics  
**Labels**: web-interface, ui/ux, frontend, tornado, real-time  
**Jira Ticket**: [DONKEY-003](JIRA_TICKETS.md#story-3-web-based-control-and-monitoring-interface)  
**Status**: In Development  

---

## Feature Overview

### Business Logic

**Problem Statement**:
Traditional robot control requires:
- Physical controllers (gamepads, joysticks) that may not be available
- SSH connections for remote operation (complex for non-technical users)
- Separate tools for monitoring and control
- Limited accessibility from different devices

**Business Value**:
- **Accessibility**: Control robot from any device with a web browser
- **User Experience**: Intuitive interface reduces learning curve
- **Remote Operation**: Operate robot without physical proximity
- **Data Collection**: Easy start/stop of training data collection
- **Demonstration**: Professional interface for presentations and demos
- **Collaboration**: Multiple users can monitor robot simultaneously

**Success Metrics**:
- Setup time: < 5 minutes to access interface
- User satisfaction: 90% find interface intuitive
- Latency: < 100ms for control input response
- Camera streaming: 15+ FPS on local network
- Mobile compatibility: Works on 95% of mobile devices

---

## Technical Architecture

### System Overview

The web interface consists of:
1. **Backend Server**: Tornado web server handling HTTP/WebSocket requests
2. **Frontend UI**: HTML/CSS/JavaScript interface
3. **Real-Time Communication**: WebSocket for bidirectional data flow
4. **Camera Streaming**: MJPEG or WebSocket-based image streaming

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│              Web Browser (Client)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   HTML/CSS   │  │  JavaScript  │  │  WebSocket   │  │
│  │   Interface  │  │   Controls   │  │   Client     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                        │
                        │ HTTP/WebSocket
                        ▼
┌─────────────────────────────────────────────────────────┐
│         Tornado Web Server (Backend)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   HTTP       │  │  WebSocket   │  │  Static      │  │
│  │   Routes     │  │  Handler     │  │  Files       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                        │
                        │ Memory Channels
                        ▼
┌─────────────────────────────────────────────────────────┐
│              Vehicle System                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Camera     │  │  Controller  │  │  Actuator    │  │
│  │   Part       │  │   Part       │  │   Part       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. Web Controller Part

**Purpose**: Bridge between web interface and vehicle system

**Implementation**: `donkeycar/parts/web_controller/web.py::LocalWebController`

**Responsibilities**:
- Start Tornado web server
- Handle HTTP requests for UI
- Manage WebSocket connections
- Process control inputs from web interface
- Stream camera images to clients
- Manage driving modes (User, Local Angle, Local Pilot)
- Control data recording

**Key Methods**:
```python
class LocalWebController:
    def __init__(self, port=8887):
        """Initialize web server on specified port"""
        
    def run_threaded(self, image_array):
        """Called by drive loop - returns user inputs"""
        # Returns: angle, throttle, mode, recording
        
    def update(self):
        """Background thread - handles web server"""
        # Runs Tornado IOLoop
```

**Web Server Setup**:
- Port: 8887 (default, configurable)
- Static files: Serves HTML, CSS, JavaScript
- WebSocket endpoint: `/ws` for real-time communication
- HTTP endpoints: `/`, `/drive`, `/api/*` for REST API

#### 2. Frontend Interface

**Purpose**: User-facing web interface

**Implementation**: `donkeycar/parts/web_controller/templates/vehicle.html`

**Components**:

1. **Camera Feed Display**
   - Real-time video stream from robot camera
   - MJPEG stream or WebSocket-based image updates
   - Full-screen option
   - Resolution: Matches camera resolution (typically 160x120)

2. **Control Interface**
   - Touch/joystick controls for steering and throttle
   - Visual joystick with drag support
   - Keyboard controls (arrow keys, WASD)
   - Gamepad support (if available)

3. **Mode Selection**
   - User Mode: Full manual control
   - Local Angle: Neural network controls steering, user controls throttle
   - Local Pilot: Full autonomous control
   - Visual indicators for current mode

4. **Data Recording Controls**
   - Start/Stop recording button
   - Recording status indicator
   - Session information display

5. **Model Management**
   - Model selection dropdown
   - Model loading status
   - Model performance metrics (if available)

6. **Telemetry Display**
   - Current steering angle
   - Current throttle value
   - Drive loop frequency
   - Connection status
   - Robot state information

**UI Framework**:
- Bootstrap 3.3.7 for responsive design
- jQuery 3.1.1 for DOM manipulation
- Custom JavaScript for controls and WebSocket
- Touch-friendly interface for mobile devices

#### 3. Real-Time Communication

**Protocol**: WebSocket for bidirectional communication

**Message Types**:

1. **Control Messages** (Client → Server):
   ```json
   {
     "msg_type": "control",
     "angle": 0.5,
     "throttle": 0.3,
     "mode": "user",
     "recording": true
   }
   ```

2. **Image Messages** (Server → Client):
   ```json
   {
     "msg_type": "image",
     "image": "base64_encoded_jpeg"
   }
   ```

3. **Telemetry Messages** (Server → Client):
   ```json
   {
     "msg_type": "telemetry",
     "angle": 0.5,
     "throttle": 0.3,
     "mode": "user",
     "recording": true,
     "fps": 20
   }
   ```

**WebSocket Handler**:
```python
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        """Client connected"""
        
    def on_message(self, message):
        """Handle message from client"""
        data = json.loads(message)
        if data['msg_type'] == 'control':
            # Update control inputs
            self.controller.update_controls(data)
            
    def on_close(self):
        """Client disconnected"""
```

---

## Implementation Details

### Web Server Initialization

**Process**:
1. Create Tornado application with routes
2. Start IOLoop in background thread
3. Register WebSocket handler
4. Serve static files (HTML, CSS, JS)
5. Handle HTTP requests

**Code Example**:
```python
class LocalWebController:
    def __init__(self, port=8887):
        self.port = port
        self.app = self.create_app()
        self.server = None
        
    def create_app(self):
        app = tornado.web.Application([
            (r"/", MainHandler),
            (r"/ws", WebSocketHandler),
            (r"/static/(.*)", tornado.web.StaticFileHandler, 
              {"path": static_path}),
        ])
        return app
        
    def update(self):
        """Run in background thread"""
        self.server = tornado.httpserver.HTTPServer(self.app)
        self.server.listen(self.port)
        tornado.ioloop.IOLoop.current().start()
```

### Camera Streaming

**Method 1: MJPEG Stream**
- Continuous JPEG stream over HTTP
- Simple implementation
- Higher latency
- Format: `multipart/x-mixed-replace`

**Method 2: WebSocket Image Updates**
- Send JPEG frames via WebSocket
- Lower latency
- More efficient
- Base64 encoded or binary

**Implementation**:
```python
def stream_image(self, image_array):
    """Send image to all connected clients"""
    # Encode image to JPEG
    _, buffer = cv2.imencode('.jpg', image_array)
    image_bytes = buffer.tobytes()
    
    # Send via WebSocket
    message = {
        'msg_type': 'image',
        'image': base64.b64encode(image_bytes).decode()
    }
    self.broadcast(message)
```

### Control Input Processing

**Process**:
1. Receive control input from web interface
2. Validate input values (angle: -1 to 1, throttle: -1 to 1)
3. Update controller state
4. Return values to drive loop via `run_threaded()`

**Code Example**:
```python
def run_threaded(self, image_array):
    """Called by drive loop"""
    # Get latest control inputs
    angle = self.angle
    throttle = self.throttle
    mode = self.mode
    recording = self.recording
    
    # Send image to clients
    self.stream_image(image_array)
    
    return angle, throttle, mode, recording
```

### Mode Switching

**Modes**:
1. **User Mode**: Web controller provides angle and throttle
2. **Local Angle Mode**: Neural network provides angle, user provides throttle
3. **Local Pilot Mode**: Neural network provides both angle and throttle

**Implementation**:
```python
def drive_mode(self, mode, user_angle, user_throttle, 
               pilot_angle, pilot_throttle):
    """Select inputs based on mode"""
    if mode == 'user':
        return user_angle, user_throttle
    elif mode == 'local_angle':
        return pilot_angle, user_throttle
    else:  # local_pilot
        return pilot_angle, pilot_throttle
```

---

## Data Flow

### Control Input Flow

```
Web Browser
    │
    │ User interacts with controls
    │ (touch, keyboard, gamepad)
    ▼
JavaScript Event Handler
    │
    │ Create control message
    ▼
WebSocket Send
    │
    │ JSON message
    ▼
Tornado WebSocket Handler
    │
    │ Update controller state
    ▼
LocalWebController.run_threaded()
    │
    │ Return angle, throttle
    ▼
Vehicle Drive Loop
    │
    │ Pass to actuator
    ▼
Motor Controller
```

### Camera Stream Flow

```
Camera Part
    │
    │ Capture image
    ▼
Memory Channel: 'cam/image_array'
    │
    │ Read image
    ▼
LocalWebController.run_threaded(image)
    │
    │ Encode to JPEG
    ▼
WebSocket Broadcast
    │
    │ Send to all clients
    ▼
Web Browser
    │
    │ Decode and display
    ▼
Canvas/IMG Element
```

---

## Technical Specifications

### Performance Requirements

- **Control Latency**: < 100ms from input to actuator
- **Camera Streaming**: 15-30 FPS (depending on network)
- **WebSocket Latency**: < 50ms for control messages
- **Concurrent Connections**: Support 5+ simultaneous viewers
- **Memory Usage**: < 50MB for web server

### Network Requirements

- **Local Network**: Works on same WiFi network
- **Port**: 8887 (default, configurable)
- **Protocol**: HTTP/WebSocket
- **Bandwidth**: ~1-2 Mbps for camera streaming
- **Firewall**: May need to allow port 8887

### Browser Compatibility

- **Desktop**: Chrome, Firefox, Safari, Edge (latest versions)
- **Mobile**: iOS Safari, Chrome Mobile, Android Browser
- **Features Required**: WebSocket, Canvas, Touch Events
- **Minimum Resolution**: 320x240 (mobile)

### Security Considerations

- **Local Network Only**: No external access by default
- **No Authentication**: Suitable for local development only
- **HTTPS**: Can be added for production use
- **Input Validation**: All inputs validated and clamped

---

## User Interface Design

### Layout

```
┌─────────────────────────────────────────┐
│         Header (Title, Status)          │
├─────────────────────────────────────────┤
│                                         │
│      ┌──────────────────────┐          │
│      │                      │          │
│      │   Camera Feed        │          │
│      │   (Live Stream)      │          │
│      │                      │          │
│      └──────────────────────┘          │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │      Control Joystick            │  │
│  │      (Steering & Throttle)       │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  Mode: [User] [Local Angle]      │  │
│  │  [Local Pilot]                   │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  Recording: [Start] [Stop]       │  │
│  │  Model: [Select Model ▼]        │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  Telemetry:                      │  │
│  │  Angle: 0.5  Throttle: 0.3      │  │
│  │  FPS: 20  Mode: user            │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Responsive Design

- **Desktop**: Full layout with all controls visible
- **Tablet**: Optimized layout, touch-friendly controls
- **Mobile**: Simplified layout, larger touch targets

---

## Usage Examples

### Example 1: Basic Web Controller Setup

```python
V = dk.Vehicle()

# Add camera
cam = dk.parts.PiCamera()
V.add(cam, outputs=['cam/image_array'], threaded=True)

# Add web controller
web_ctr = dk.parts.LocalWebController(port=8887)
V.add(web_ctr,
      inputs=['cam/image_array'],
      outputs=['user/angle', 'user/throttle', 'user/mode', 'recording'],
      threaded=True)

# Add actuator
actuator = dk.parts.PCA9685()
V.add(actuator,
      inputs=['user/angle', 'user/throttle'],
      outputs=['motor/left', 'motor/right'])

V.start()
# Access at http://localhost:8887
```

### Example 2: Web Controller with Autopilot

```python
V = dk.Vehicle()

# Add camera
cam = dk.parts.PiCamera()
V.add(cam, outputs=['cam/image_array'], threaded=True)

# Add web controller
web_ctr = dk.parts.LocalWebController()
V.add(web_ctr,
      inputs=['cam/image_array'],
      outputs=['user/angle', 'user/throttle', 'user/mode', 'recording'],
      threaded=True)

# Add neural network pilot
kl = dk.parts.KerasLinear()
kl.load('./models/mypilot.h5')
V.add(kl,
      inputs=['cam/image_array'],
      outputs=['pilot/angle', 'pilot/throttle'],
      run_condition='run_pilot')

# Mode switching logic
def drive_mode(mode, user_angle, user_throttle, 
               pilot_angle, pilot_throttle):
    if mode == 'user':
        return user_angle, user_throttle
    elif mode == 'local_angle':
        return pilot_angle, user_throttle
    else:
        return pilot_angle, pilot_throttle

mode_switch = dk.parts.Lambda(drive_mode)
V.add(mode_switch,
      inputs=['user/mode', 'user/angle', 'user/throttle',
              'pilot/angle', 'pilot/throttle'],
      outputs=['angle', 'throttle'])

# Add actuator
actuator = dk.parts.PCA9685()
V.add(actuator, inputs=['angle', 'throttle'])

V.start()
```

---

## Testing Strategy

### Unit Tests

- Test web server initialization
- Test WebSocket message handling
- Test control input processing
- Test image encoding/streaming
- Test mode switching logic

### Integration Tests

- Test end-to-end control flow
- Test camera streaming performance
- Test concurrent connections
- Test mobile device compatibility

### User Acceptance Tests

- Test interface usability
- Test control responsiveness
- Test on different devices/browsers
- Test in different network conditions

---

## Dependencies

### Backend Dependencies
- Tornado 4.5.3 (web server)
- NumPy (image processing)
- PIL/Pillow (image encoding)
- OpenCV (optional, for image processing)

### Frontend Dependencies
- Bootstrap 3.3.7 (CSS framework)
- jQuery 3.1.1 (JavaScript library)
- Custom JavaScript (controls, WebSocket)

---

## Future Enhancements

1. **Authentication**: User login and access control
2. **HTTPS Support**: Secure connections
3. **Multi-Robot View**: Monitor multiple robots simultaneously
4. **Advanced Telemetry**: Charts, graphs, historical data
5. **Mobile App**: Native mobile application
6. **Cloud Integration**: Remote access via cloud service
7. **Video Recording**: Record and playback driving sessions
8. **Customizable UI**: User-configurable interface layouts
9. **Real-Time Analytics**: Performance metrics and analysis
10. **Social Features**: Share driving sessions, leaderboards

---

## Related Documentation

- [Main Project Documentation](CONFLUENCE_PAGE.md)
- [Getting Started Guide](docs/guide/get_driving.md)
- [Web Controller API](donkeycar/parts/web_controller/web.py)
- [Tornado Documentation](https://www.tornadoweb.org/)

---

**Last Updated**: [Date]  
**Page Owner**: Engineering Team  
**Review Frequency**: Quarterly

