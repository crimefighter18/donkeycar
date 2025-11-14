# Quasiboto Donkeycar - Key Features

## Feature List

### Feature 1: Modular Parts Architecture
**Description**: A flexible, plug-and-play component system that allows users to easily add, remove, or customize robot components.

**Details**:
- Each component (sensor, actuator, controller, pilot) is a standalone Python class
- Components communicate through a shared memory channel system
- Supports both threaded and non-threaded execution modes
- Simple API: `V.add(part, inputs=[], outputs=[])` to add components
- Components can be hot-swapped and reconfigured without code changes

**Benefits**:
- Rapid prototyping and experimentation
- Easy to extend with custom hardware
- Simplified debugging and testing
- Reusable components across different robot configurations

**Use Cases**:
- Adding new sensors (LIDAR, GPS, IMU)
- Integrating different motor controllers
- Switching between different neural network models
- Adding data logging or processing components

---

### Feature 2: Neural Network Autopilot with Behavioral Cloning
**Description**: Train and deploy deep learning models for autonomous navigation using behavioral cloning techniques.

**Details**:
- Collects training data during manual driving sessions (images + control inputs)
- Supports Keras/TensorFlow neural network models
- Multiple model architectures: Linear, Categorical, RNN, 3D CNN
- Real-time inference during autonomous driving
- Model switching and A/B testing capabilities

**Benefits**:
- Learn autonomous navigation from human demonstrations
- No need for complex path planning algorithms
- Adaptable to different tracks and environments
- Can leverage community-shared models and datasets

**Use Cases**:
- Training on specific race tracks
- Learning obstacle avoidance behaviors
- Adapting to different lighting conditions
- Competing in autonomous racing competitions

---

### Feature 3: Web-Based Control and Monitoring Interface
**Description**: A comprehensive browser-based interface for controlling the robot, monitoring its state, and managing data collection.

**Details**:
- Real-time camera feed streaming
- Touch/joystick controls for manual driving
- Mode switching (User, Local Angle, Local Pilot)
- Throttle and steering calibration controls
- Data recording start/stop functionality
- Model selection and deployment
- Real-time telemetry display

**Benefits**:
- No need for physical controllers or SSH connections
- Accessible from any device on the network
- Easy to use for non-technical users
- Centralized control and monitoring

**Use Cases**:
- Remote robot operation
- Training data collection sessions
- Testing and debugging autonomous behavior
- Demonstrations and presentations
- Multi-user collaboration

---

## Additional Notable Features

- **Differential Steering Support**: Specialized motor control for tank-style robots
- **Data Logging (Tub System)**: Efficient storage of images, sensor data, and control inputs
- **Simulator Integration**: Test models in simulation before deploying to hardware
- **Multi-Platform Support**: Works on Raspberry Pi, Linux, macOS, and Windows
- **Community Data Sharing**: Leverage datasets from other users
- **Extensive Documentation**: Comprehensive guides for hardware and software setup

