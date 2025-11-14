# Quasiboto Donkeycar - Autonomous Robot Platform

## Project Overview

**Quasiboto Donkeycar** is a Python-based self-driving library specifically designed for the Quasiboto Open Source Robot Platform. This project is a fork of the popular Donkeycar framework, adapted to support differential/tank steering mechanisms commonly used in robotics applications.

The library provides a minimalist, modular architecture that enables hobbyists, students, and researchers to build autonomous robots capable of self-driving, data collection, and machine learning-based navigation.

## What is This Project?

This project is an autonomous driving framework that transforms a Quasiboto robot into a self-driving vehicle. It combines:

- **Hardware Integration**: Seamless connection with cameras, motor controllers, sensors, and actuators
- **Software Framework**: Modular Python library for building autonomous driving systems
- **Machine Learning**: Support for training neural network-based autopilots using behavioral cloning
- **Data Collection**: Comprehensive logging system for images, sensor data, and control inputs
- **Web Interface**: Browser-based control and monitoring system

## Key Capabilities

### 1. Modular Architecture
The system is built around a "parts" concept where each component (camera, motor controller, neural network, etc.) is a standalone, pluggable module. This allows for:
- Easy customization and extension
- Rapid prototyping and experimentation
- Simple debugging and maintenance

### 2. Differential/Tank Steering Support
Unlike traditional car steering, this fork supports differential drive systems where:
- Left and right motors are controlled independently
- Steering is achieved through differential motor speeds
- Ideal for tank-style robots and differential drive platforms

### 3. Autonomous Navigation
The system supports multiple driving modes:
- **User Mode**: Manual control via web interface or game controller
- **Local Angle Mode**: Neural network controls steering, user controls throttle
- **Local Pilot Mode**: Fully autonomous control by trained neural network

### 4. Data Collection & Training
- Records camera images, control inputs, and sensor readings
- Stores data in "tub" format for easy processing
- Supports training neural networks using behavioral cloning
- Enables model training on collected driving data

### 5. Web-Based Control Interface
- Accessible at `http://localhost:8887`
- Real-time camera feed
- Manual driving controls
- Mode switching and configuration
- Data recording controls

## Technology Stack

- **Language**: Python 3.5+
- **Deep Learning**: TensorFlow/Keras for neural network models
- **Web Framework**: Tornado for web interface
- **Computer Vision**: OpenCV, PIL for image processing
- **Hardware**: Raspberry Pi, PiCamera, motor controllers (PCA9685, Piconzero)

## Project Structure

```
donkeycar/
├── donkeycar/          # Main library code
│   ├── parts/          # Modular components (camera, actuators, etc.)
│   ├── management/     # CLI tools and data management
│   ├── templates/      # Vehicle configuration templates
│   └── vehicle.py      # Core vehicle class
├── docs/               # Documentation
├── install/            # Installation scripts
└── tests/              # Unit tests
```

## Quick Start

1. **Hardware Setup**: Assemble your Quasiboto robot with camera, motors, and controller
2. **Software Installation**: Install Python dependencies and donkeycar library
3. **Calibration**: Calibrate steering and throttle controls
4. **Drive**: Start the vehicle and access web interface at `http://localhost:8887`
5. **Collect Data**: Record driving sessions for training
6. **Train Model**: Train a neural network autopilot on collected data
7. **Autonomous Mode**: Deploy trained model for self-driving

## Use Cases

- **Education**: Learn autonomous systems, computer vision, and machine learning
- **Research**: Experiment with different neural network architectures and algorithms
- **Competition**: Participate in self-driving robot races like DIY Robocars
- **Prototyping**: Rapidly prototype autonomous navigation systems
- **Data Collection**: Gather real-world driving data for ML research

## Development Philosophy

The project follows these core principles:

- **Modularity**: Components are standalone and independently configurable
- **Minimalism**: Each component is kept simple (<100 lines when possible)
- **Extensibility**: New components can be easily added by following templates
- **Transparency**: Code is readable and understandable without "black magic"

## Community & Resources

- **Original Donkeycar**: [donkeycar.com](http://donkeycar.com)
- **Documentation**: [docs.donkeycar.com](http://docs.donkeycar.com)
- **Quasiboto Repository**: [GitHub](https://github.com/mtedder/Quasiboto)
- **Community**: Join the Slack channel for support and discussions

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! The project encourages:
- Adding new parts/components
- Improving documentation
- Fixing bugs
- Sharing driving data and models

---

**Note**: This is a specialized fork for Quasiboto robots with differential steering. For standard RC car applications, see the main [Donkeycar repository](https://github.com/autorope/donkeycar).

