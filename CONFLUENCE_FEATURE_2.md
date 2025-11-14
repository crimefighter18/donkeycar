# Confluence: Feature 2 - Neural Network Autopilot with Behavioral Cloning

**Page Type**: Feature Documentation  
**Space**: Engineering / Robotics  
**Labels**: machine-learning, neural-networks, autopilot, keras, tensorflow  
**Jira Ticket**: [DONKEY-002](JIRA_TICKETS.md#story-2-neural-network-autopilot-with-behavioral-cloning)  
**Status**: In Development  

---

## Feature Overview

### Business Logic

**Problem Statement**:
Traditional autonomous navigation systems require complex algorithms for path planning, obstacle detection, and control. These approaches are:
- Difficult to implement and tune
- Require extensive domain knowledge
- Don't adapt well to different environments
- Hard to modify for specific use cases

**Business Value**:
- **Easier Implementation**: Learn from demonstrations rather than hand-coding algorithms
- **Adaptability**: Models adapt to different tracks and environments through training
- **Accessibility**: Non-experts can create autonomous systems by providing training data
- **Competitive Advantage**: Enables participation in autonomous racing competitions
- **Research Platform**: Foundation for experimenting with different ML approaches

**Success Metrics**:
- Model training time: < 2 hours for 10,000 images
- Autonomous driving success rate: > 80% on training track
- Model inference latency: < 50ms on Raspberry Pi 4
- User satisfaction: 90% of users successfully train a working model

---

## Technical Architecture

### Behavioral Cloning Overview

**Concept**: The robot learns to drive by observing human demonstrations. During manual driving, the system records:
- Camera images (what the robot sees)
- Control inputs (steering angle, throttle - what the human did)

The neural network learns the mapping: `Image → Control Actions`

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Data Collection Phase                       │
│                                                          │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐     │
│  │  Camera  │─────▶│  Memory  │─────▶│   Tub    │     │
│  │  Part    │      │ Channels │      │  Storage │     │
│  └──────────┘      └──────────┘      └──────────┘     │
│       │                  │                  │           │
│       │                  │                  │           │
│       └──────────────────┴──────────────────┘           │
│                    Manual Driving                       │
└─────────────────────────────────────────────────────────┘
                        │
                        │ Training Data
                        ▼
┌─────────────────────────────────────────────────────────┐
│              Model Training Phase                        │
│                                                          │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐     │
│  │   Tub    │─────▶│  Data    │─────▶│  Neural  │     │
│  │  Reader  │      │ Preproc  │      │ Network  │     │
│  └──────────┘      └──────────┘      └──────────┘     │
│                              │                          │
│                              ▼                          │
│                       ┌──────────┐                      │
│                       │  Model   │                      │
│                       │  Saved   │                      │
│                       └──────────┘                      │
└─────────────────────────────────────────────────────────┘
                        │
                        │ Trained Model
                        ▼
┌─────────────────────────────────────────────────────────┐
│              Autonomous Driving Phase                    │
│                                                          │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐     │
│  │  Camera  │─────▶│  Neural  │─────▶│ Actuator │     │
│  │  Part    │      │ Network  │      │   Part   │     │
│  │          │      │ Inference│      │          │     │
│  └──────────┘      └──────────┘      └──────────┘     │
│       │                  │                  │           │
│       │                  │                  │           │
│       └──────────────────┴──────────────────┘           │
│                    Autonomous Loop                      │
└─────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. Data Collection System

**Purpose**: Record images and control inputs during manual driving

**Implementation**: `donkeycar/parts/datastore.py` (Tub system)

**Data Format**:
- Images: JPEG files stored in `images/` directory
- Metadata: JSON records with image path, angle, throttle, timestamp
- Structure:
  ```
  tub_1/
  ├── images/
  │   ├── 1_cam-image_array_.jpg
  │   ├── 2_cam-image_array_.jpg
  │   └── ...
  ├── meta.json
  └── manifest.json
  ```

**Collection Process**:
1. User drives robot manually via web interface
2. Camera part captures images at drive loop frequency
3. Controller part captures user inputs (angle, throttle)
4. Tub part writes image + metadata to disk
5. Process repeats for entire driving session

**Code Example**:
```python
# During manual driving
tub = dk.parts.Tub(path='./data/tub_1',
                   inputs=['cam/image_array', 'user/angle', 'user/throttle'],
                   types=['image_array', 'float', 'float'])
V.add(tub, inputs=['cam/image_array', 'user/angle', 'user/throttle'])
```

#### 2. Training Pipeline

**Purpose**: Process collected data and train neural network models

**Implementation**: `donkeycar/management/train.py`

**Training Process**:
1. **Data Loading**: Read images and metadata from tub directories
2. **Data Augmentation**: Apply transformations (flip, brightness, etc.)
3. **Data Splitting**: Train/validation split (typically 80/20)
4. **Model Definition**: Create neural network architecture
5. **Training**: Fit model on training data with validation monitoring
6. **Model Saving**: Save trained model weights and architecture

**Training Command**:
```bash
python manage.py train \
    --tub ./data/tub_1,./data/tub_2 \
    --model ./models/mypilot \
    --type linear
```

**Training Parameters**:
- Batch size: 128 (default)
- Epochs: 100 (default, with early stopping)
- Learning rate: 0.001 (default)
- Validation split: 0.2 (20%)

#### 3. Model Architectures

**Supported Types**:

1. **Linear Model** (`donkeycar/parts/keras.py::KerasLinear`)
   - Simple regression model
   - Output: Continuous steering angle and throttle
   - Architecture: CNN → Flatten → Dense layers
   - Use case: Basic autonomous driving

2. **Categorical Model** (`donkeycar/parts/keras.py::KerasCategorical`)
   - Classification-based steering
   - Output: Probability distribution over steering angles
   - Architecture: CNN → Flatten → Dense → Softmax
   - Use case: More stable steering control

3. **RNN Model** (`donkeycar/parts/keras.py::KerasRNN`)
   - Recurrent neural network
   - Output: Sequential predictions
   - Architecture: CNN → LSTM/GRU → Dense
   - Use case: Temporal pattern learning

4. **3D CNN Model** (`donkeycar/parts/keras.py::Keras3D`)
   - Spatiotemporal model
   - Input: Video sequences
   - Architecture: 3D CNN layers
   - Use case: Motion-aware predictions

**Model Architecture Example (Linear)**:
```python
def default_linear():
    model = Sequential()
    model.add(Conv2D(24, (5, 5), strides=(2, 2), 
                     activation='relu', input_shape=(120, 160, 3)))
    model.add(Conv2D(32, (5, 5), strides=(2, 2), activation='relu'))
    model.add(Conv2D(64, (3, 3), strides=(2, 2), activation='relu'))
    model.add(Conv2D(64, (3, 3), strides=(1, 1), activation='relu'))
    model.add(Flatten())
    model.add(Dense(100, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(2))  # [angle, throttle]
    return model
```

#### 4. Model Inference Part

**Purpose**: Load trained model and make real-time predictions during autonomous driving

**Implementation**: `donkeycar/parts/keras.py::KerasLinear` (and other model types)

**Inference Process**:
1. Load model from disk on initialization
2. Receive camera image from memory channel
3. Preprocess image (resize, normalize)
4. Run inference through neural network
5. Post-process outputs (denormalize, clip values)
6. Write predictions to memory channels

**Code Example**:
```python
# During autonomous driving
kl = KerasLinear()
kl.load('./models/mypilot.h5')
V.add(kl,
      inputs=['cam/image_array'],
      outputs=['pilot/angle', 'pilot/throttle'],
      run_condition='run_pilot')
```

**Performance**:
- Inference time: 20-50ms on Raspberry Pi 4
- Throughput: 20-50 FPS (depending on model complexity)
- Memory usage: ~200MB for model weights

---

## Data Flow

### Training Data Flow

```
Manual Driving Session
    │
    ├─▶ Camera captures image
    │       │
    │       ▼
    │   Image stored to disk
    │
    ├─▶ User provides control input
    │       │
    │       ▼
    │   Angle/Throttle recorded
    │
    └─▶ Metadata written to JSON
            │
            ▼
    Tub directory with images + metadata
```

### Training Pipeline Flow

```
Tub Directories
    │
    ├─▶ Load images and metadata
    │       │
    │       ▼
    │   Apply data augmentation
    │       │
    │       ▼
    │   Split train/validation
    │       │
    │       ▼
    └─▶ Train neural network
            │
            ▼
    Trained model saved
```

### Inference Flow

```
Camera Image
    │
    ▼
Preprocess (resize, normalize)
    │
    ▼
Neural Network Inference
    │
    ▼
Post-process (denormalize, clip)
    │
    ▼
Steering Angle + Throttle
    │
    ▼
Actuator Part (motors)
```

---

## Technical Specifications

### Data Collection

- **Image Format**: JPEG, typically 160x120 or 120x160 pixels
- **Frame Rate**: 10-30 Hz (matches drive loop frequency)
- **Storage**: ~1MB per second of driving data
- **Metadata**: JSON format with image path, angle, throttle, timestamp

### Model Training

- **Framework**: Keras/TensorFlow
- **Input Size**: Configurable (default 120x160x3)
- **Output Size**: 2 values (angle, throttle) for linear models
- **Training Time**: 1-3 hours for 10,000 images on CPU, 10-30 minutes on GPU
- **Model Size**: 5-50MB depending on architecture

### Model Inference

- **Latency**: < 50ms on Raspberry Pi 4
- **Throughput**: 20-50 FPS
- **Memory**: ~200MB for model + inference
- **Precision**: Float32 (can be quantized to Float16 or Int8)

### Performance Optimization

**Techniques**:
1. **Image Preprocessing**: Resize to smaller dimensions before inference
2. **Model Quantization**: Reduce precision (Float32 → Float16 → Int8)
3. **Model Pruning**: Remove unnecessary weights
4. **TensorFlow Lite**: Convert to TFLite for mobile deployment
5. **Batch Processing**: Process multiple frames (if applicable)

---

## Training Best Practices

### Data Collection

1. **Quality over Quantity**: 5,000 good images > 20,000 bad images
2. **Diverse Scenarios**: Include turns, straights, recovery from errors
3. **Consistent Driving**: Smooth, consistent control inputs
4. **Multiple Sessions**: Collect data across different times/conditions
5. **Remove Bad Data**: Delete frames with poor driving or errors

### Training Tips

1. **Start Simple**: Use linear model first, then try categorical
2. **Monitor Validation Loss**: Stop training when validation loss plateaus
3. **Data Augmentation**: Enable to improve generalization
4. **Learning Rate**: Start with 0.001, adjust if needed
5. **Early Stopping**: Prevent overfitting

### Model Selection

- **Linear**: Best for beginners, fast training, good baseline
- **Categorical**: More stable steering, better for racing
- **RNN**: Better for temporal patterns, slower inference
- **3D CNN**: Best for motion-aware driving, requires more data

---

## Usage Examples

### Example 1: Collect Training Data

```python
# In vehicle configuration
V = dk.Vehicle()

# Add camera
cam = dk.parts.PiCamera()
V.add(cam, outputs=['cam/image_array'], threaded=True)

# Add controller
ctr = dk.parts.LocalWebController()
V.add(ctr, outputs=['user/angle', 'user/throttle'], threaded=True)

# Add data collection
tub = dk.parts.Tub(path='./data/tub_1',
                   inputs=['cam/image_array', 'user/angle', 'user/throttle'],
                   types=['image_array', 'float', 'float'])
V.add(tub, inputs=['cam/image_array', 'user/angle', 'user/throttle'])

V.start()
```

### Example 2: Train Model

```bash
# Train linear model
python manage.py train \
    --tub ./data/tub_1,./data/tub_2 \
    --model ./models/mypilot \
    --type linear \
    --epochs 100 \
    --batch_size 128
```

### Example 3: Deploy Model for Autonomous Driving

```python
# In vehicle configuration
V = dk.Vehicle()

# Add camera
cam = dk.parts.PiCamera()
V.add(cam, outputs=['cam/image_array'], threaded=True)

# Add trained model
kl = dk.parts.KerasLinear()
kl.load('./models/mypilot.h5')
V.add(kl,
      inputs=['cam/image_array'],
      outputs=['pilot/angle', 'pilot/throttle'],
      run_condition='run_pilot')

# Add actuator
actuator = dk.parts.PCA9685()
V.add(actuator,
      inputs=['pilot/angle', 'pilot/throttle'],
      outputs=['motor/left', 'motor/right'])

V.start()
```

---

## Testing Strategy

### Unit Tests

- Test data loading from tub
- Test data augmentation
- Test model architecture creation
- Test model saving/loading
- Test inference on sample images

### Integration Tests

- Test end-to-end training pipeline
- Test model deployment in vehicle
- Test inference performance
- Test mode switching (user vs pilot)

### Validation Tests

- Test model accuracy on validation set
- Test autonomous driving on test track
- Test model robustness to different conditions

---

## Dependencies

### Core Dependencies
- TensorFlow >= 1.9.0 or TensorFlow 2.x
- Keras (included with TensorFlow)
- NumPy
- PIL/Pillow
- H5py (for model saving)

### Optional Dependencies
- TensorFlow Lite (for mobile deployment)
- TensorRT (for NVIDIA GPU acceleration)

---

## Future Enhancements

1. **Transfer Learning**: Pre-trained models for faster training
2. **Online Learning**: Update model during driving
3. **Ensemble Models**: Combine multiple models for better performance
4. **Reinforcement Learning**: RL-based training in addition to behavioral cloning
5. **Sim-to-Real**: Train in simulator, deploy to real robot
6. **Model Compression**: Automatic model optimization for edge devices
7. **A/B Testing**: Compare multiple models in real-time

---

## Related Documentation

- [Main Project Documentation](CONFLUENCE_PAGE.md)
- [Training Guide](docs/guide/train_autopilot.md)
- [Keras Parts API](donkeycar/parts/keras.py)
- [Data Storage System](donkeycar/parts/datastore.py)

---

**Last Updated**: [Date]  
**Page Owner**: Engineering Team  
**Review Frequency**: Quarterly

