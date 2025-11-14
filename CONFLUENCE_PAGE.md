# Confluence Page: Quasiboto Donkeycar Project

---

# Quasiboto Donkeycar - Autonomous Robot Platform

**Page Type**: Project Documentation  
**Space**: Engineering / Robotics  
**Labels**: autonomous-vehicles, robotics, python, machine-learning, open-source  

---

## Executive Summary

**Quasiboto Donkeycar** is an open-source Python framework that transforms Quasiboto robots into autonomous self-driving vehicles. Built on a modular architecture, the platform enables rapid development of autonomous navigation systems through behavioral cloning and neural network-based autopilots.

**Project Status**: Active Development  
**Version**: 2.5.7  
**License**: MIT  
**Repository**: [GitHub Repository Link]  

---

## Project Overview

### What is Quasiboto Donkeycar?

Quasiboto Donkeycar is a specialized fork of the popular Donkeycar framework, adapted for the Quasiboto Open Source Robot Platform. Unlike traditional autonomous car projects that use steering wheels, this framework supports **differential/tank steering** mechanisms, making it ideal for robotics applications.

### Core Purpose

The project aims to:
- Democratize autonomous robotics development
- Provide an educational platform for learning AI and robotics
- Enable rapid prototyping of self-driving systems
- Support research and competition in autonomous robotics

---

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    Vehicle Core                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  Memory  │  │  Drive   │  │  Parts   │             │
│  │ Channels │  │   Loop   │  │ Manager  │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└─────────────────────────────────────────────────────────┘
         │              │              │
    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
    │ Sensors │    │Actuators│    │ Pilots  │
    │         │    │         │    │         │
    │ Camera  │    │ Motors  │    │ Neural  │
    │ IMU     │    │ Servos  │    │ Network │
    │ GPS     │    │         │    │         │
    └─────────┘    └─────────┘    └─────────┘
```

### Key Architectural Principles

1. **Modularity**: Each component is a standalone, pluggable part
2. **Minimalism**: Components are simple and transparent (<100 lines when possible)
3. **Extensibility**: New parts can be added by following templates
4. **Python-First**: Pure Python implementation for simplicity

---

## Feature Documentation

This project includes three core features. Each feature has detailed technical and business documentation:

### [Feature 1: Modular Parts Architecture](CONFLUENCE_FEATURE_1.md)
A flexible, plug-and-play component system that allows users to easily add, remove, or customize robot components without modifying core vehicle code.

**Key Benefits**: Rapid prototyping, easy customization, simplified maintenance

**Jira Ticket**: [DONKEY-001](JIRA_TICKETS.md#story-1-modular-parts-architecture)

---

### [Feature 2: Neural Network Autopilot with Behavioral Cloning](CONFLUENCE_FEATURE_2.md)
Train and deploy deep learning models for autonomous navigation using behavioral cloning techniques. The system learns from human driving demonstrations.

**Key Benefits**: Easier implementation, adaptability, accessibility for non-experts

**Jira Ticket**: [DONKEY-002](JIRA_TICKETS.md#story-2-neural-network-autopilot-with-behavioral-cloning)

---

### [Feature 3: Web-Based Control and Monitoring Interface](CONFLUENCE_FEATURE_3.md)
A comprehensive browser-based interface for controlling the robot, monitoring its state, and managing data collection. Accessible from any device with a web browser.

**Key Benefits**: Accessibility, remote operation, intuitive user experience

**Jira Ticket**: [DONKEY-003](JIRA_TICKETS.md#story-3-web-based-control-and-monitoring-interface)

---

For detailed technical specifications, implementation details, and business logic for each feature, please refer to the individual feature documentation pages linked above.

---

## Technical Specifications

### System Requirements

**Hardware**:
- Quasiboto robot platform
- Raspberry Pi 3/4 (recommended)
- Camera (PiCamera or USB webcam)
- Motor controller (PCA9685, Piconzero, or compatible)
- Differential drive motors

**Software**:
- Python 3.5+
- TensorFlow 1.9+ or TensorFlow 2.x
- OpenCV
- NumPy, PIL, Pandas
- Tornado web framework

### Performance Characteristics

- **Drive Loop Frequency**: 10-30 Hz
- **Camera Resolution**: Configurable (default 160x120)
- **Model Inference**: <50ms latency on Raspberry Pi 4
- **Data Storage**: ~1MB per second of driving data

---

## Getting Started

### Quick Start Guide

1. **Hardware Assembly**
   - Follow [Hardware Build Guide](docs/guide/build_hardware.md)
   - Assemble Quasiboto robot with camera and motors
   - Connect motor controller to Raspberry Pi

2. **Software Installation**
   ```bash
   git clone https://github.com/[repo]/donkeycar
   cd donkeycar
   pip install -e .
   ```

3. **Initial Setup**
   ```bash
   donkey createcar --path ~/mycar
   ```

4. **Calibration**
   - Follow [Calibration Guide](docs/guide/calibrate.md)
   - Calibrate steering and throttle ranges

5. **First Drive**
   ```bash
   cd ~/mycar
   python manage.py drive
   ```
   - Open browser to `http://localhost:8887`
   - Start driving and collecting data

6. **Train Autopilot**
   ```bash
   python manage.py train --tub ./data/tub_1 --model ./models/mypilot
   ```

7. **Autonomous Mode**
   ```bash
   python manage.py drive --model ./models/mypilot
   ```

---

## Project Roadmap

### Current Sprint Goals
- ✅ Modular parts architecture implementation
- 🔄 Neural network training pipeline
- 🔄 Web interface development
- ⏳ Differential steering algorithms
- ⏳ Comprehensive documentation

### Future Enhancements
- Simulator integration improvements
- Advanced neural network architectures
- Multi-robot coordination
- Cloud-based training infrastructure
- Enhanced sensor fusion (LIDAR, GPS, IMU)

---

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Keep parts under 100 lines when possible
- Use type hints where appropriate
- Document all public APIs

### Testing
- Unit tests for all parts
- Integration tests for vehicle assembly
- Hardware-in-the-loop testing for actuators

### Contribution Process
1. Fork repository
2. Create feature branch
3. Write tests for new functionality
4. Submit pull request with description

---

## Resources and Links

### Documentation
- [Main Documentation Site](http://docs.donkeycar.com)
- [API Reference](docs/)
- [FAQ](docs/faq.md)

### Community
- [Slack Channel](http://www.donkeycar.com/community.html)
- [GitHub Issues](https://github.com/[repo]/donkeycar/issues)
- [DIY Robocars](http://diyrobocars.com)

### Related Projects
- [Original Donkeycar](https://github.com/autorope/donkeycar)
- [Quasiboto Platform](https://github.com/mtedder/Quasiboto)

---

## Team and Contacts

**Project Maintainer**: [Name]  
**Email**: [email]  
**Slack**: #quasiboto-donkeycar  

---

## Changelog

### Version 2.5.7
- Initial Quasiboto fork
- Differential steering support
- Updated documentation

---

**Last Updated**: [Date]  
**Page Owner**: Engineering Team  
**Review Frequency**: Monthly

