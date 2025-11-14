# Jira Tickets for Quasiboto Donkeycar Project

## Epic: Quasiboto Donkeycar Autonomous Robot Platform

**Epic Name**: Quasiboto Donkeycar - Self-Driving Robot Framework  
**Epic Key**: DONKEY-EPIC-001  
**Type**: Epic  
**Priority**: High  
**Status**: In Progress  

**Description**:
Develop and maintain a Python-based self-driving library for the Quasiboto Open Source Robot Platform. This framework enables autonomous navigation through modular architecture, neural network-based autopilots, and comprehensive data collection capabilities.

**Acceptance Criteria**:
- Framework supports differential/tank steering mechanisms
- Modular parts system allows easy component integration
- Web interface provides control and monitoring capabilities
- Neural network training pipeline is functional
- Documentation is complete and up-to-date

---

## Story 1: Modular Parts Architecture

**Story Key**: DONKEY-001  
**Type**: Story  
**Priority**: High  
**Status**: To Do  
**Epic Link**: DONKEY-EPIC-001  
**Sprint**: Current Sprint  

**Title**: Implement Modular Parts Architecture System

**Summary**:
As a developer, I want to use a modular parts architecture so that I can easily add, remove, and configure robot components without modifying core vehicle code. This will enable rapid prototyping, easy customization, and simplified maintenance of autonomous robot systems.

**Acceptance Criteria**:
- [ ] Vehicle class supports adding parts via `V.add()` method
- [ ] Parts communicate through shared memory channel system
- [ ] Support for both threaded and non-threaded part execution
- [ ] Parts can specify inputs and outputs for data flow
- [ ] Example parts (camera, actuator, controller) are implemented
- [ ] Documentation includes guide for creating custom parts

**Story Points**: 8  
**Labels**: architecture, core-feature, python  
**Confluence Link**: [Feature 1: Modular Parts Architecture](CONFLUENCE_FEATURE_1.md)

---

## Story 2: Neural Network Autopilot with Behavioral Cloning

**Story Key**: DONKEY-002  
**Type**: Story  
**Priority**: High  
**Status**: To Do  
**Epic Link**: DONKEY-EPIC-001  
**Sprint**: Current Sprint  

**Title**: Implement Neural Network Autopilot Training and Deployment

**Summary**:
As a user, I want to train a neural network autopilot using behavioral cloning so that my robot can drive autonomously after learning from my manual driving sessions. The system should support data collection, model training, and real-time autonomous navigation.

**Acceptance Criteria**:
- [ ] Data collection system records images and control inputs during manual driving
- [ ] Training pipeline processes collected data and trains neural network models
- [ ] Support for multiple model architectures (Linear, Categorical, RNN, 3D CNN)
- [ ] Model loading and inference during autonomous driving
- [ ] Mode switching between user control and autopilot
- [ ] Model performance metrics and validation

**Story Points**: 13  
**Labels**: machine-learning, autopilot, keras, tensorflow  
**Confluence Link**: [Feature 2: Neural Network Autopilot](CONFLUENCE_FEATURE_2.md)

---

## Story 3: Web-Based Control and Monitoring Interface

**Story Key**: DONKEY-003  
**Type**: Story  
**Priority**: High  
**Status**: To Do  
**Epic Link**: DONKEY-EPIC-001  
**Sprint**: Current Sprint  

**Title**: Develop Web-Based Control and Monitoring Interface

**Summary**:
As a user, I want a web-based interface to control my robot, view camera feed, and manage autonomous driving modes so that I can operate the robot from any device without physical controllers. This will enable remote operation, easy data collection, and simplified user interaction.

**Acceptance Criteria**:
- [ ] Web server accessible at configurable port (default 8887)
- [ ] Real-time camera feed streaming
- [ ] Touch/joystick controls for steering and throttle
- [ ] Mode switching UI (User, Local Angle, Local Pilot)
- [ ] Data recording controls (start/stop)
- [ ] Model selection and deployment interface
- [ ] Responsive design works on desktop and mobile
- [ ] Real-time telemetry display

**Story Points**: 10  
**Labels**: web-interface, ui/ux, tornado, frontend  
**Confluence Link**: [Feature 3: Web-Based Control Interface](CONFLUENCE_FEATURE_3.md)

---

## Additional Tasks

### Task: Differential Steering Implementation
**Task Key**: DONKEY-004  
**Type**: Task  
**Priority**: Medium  
**Status**: To Do  
**Parent**: DONKEY-EPIC-001  

**Description**:
Implement differential/tank steering motor control algorithms for Quasiboto robots. Convert steering and throttle inputs into left/right motor speeds.

**Story Points**: 5

---

### Task: Data Logging System (Tub)
**Task Key**: DONKEY-005  
**Type**: Task  
**Priority**: Medium  
**Status**: To Do  
**Parent**: DONKEY-EPIC-001  

**Description**:
Implement efficient data storage system for images, sensor readings, and control inputs. Support data retrieval and processing for training.

**Story Points**: 5

---

### Task: Documentation and Setup Guides
**Task Key**: DONKEY-006  
**Type**: Task  
**Priority**: Medium  
**Status**: To Do  
**Parent**: DONKEY-EPIC-001  

**Description**:
Create comprehensive documentation including hardware setup, software installation, calibration, and usage guides.

**Story Points**: 3

---

## Sprint Planning Notes

**Sprint Goal**: Establish core framework with modular architecture, basic autopilot training, and web interface.

**Dependencies**:
- DONKEY-001 should be completed first (foundation for other features)
- DONKEY-002 depends on data collection from DONKEY-005
- DONKEY-003 can be developed in parallel

**Risks**:
- Hardware compatibility issues with different Quasiboto configurations
- Neural network training performance on Raspberry Pi
- Real-time camera streaming performance

