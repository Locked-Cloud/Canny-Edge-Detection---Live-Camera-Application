# Canny-Edge-Detection---Live-Camera-Application
# Canny Edge Detection - Live Camera Application

A real-time camera application that implements the **Canny Edge Detection algorithm** based on the CSE281 Image Processing course lecture materials.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Description

This project implements the complete Canny edge detection algorithm from scratch using the exact code and methodology from **Lecture 7 - Image Processing (CSE281)** by Dr. Mahmoud Zaki. The application captures live video from your webcam and applies edge detection in real-time, allowing you to see the original and processed images side by side.

## 🎯 Features

- **Live camera feed** with real-time edge detection
- **Side-by-side comparison** of original and edge-detected images
- **Interactive threshold adjustment** using keyboard controls
- **Complete implementation** of all 5 Canny algorithm steps:
  1. Noise Reduction (Gaussian Blur)
  2. Gradient Calculation (Sobel Operators)
  3. Non-Maximum Suppression
  4. Double Threshold
  5. Edge Tracking by Hysteresis

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- Webcam/Camera

### Required Libraries

```bash
pip install numpy opencv-python scikit-image matplotlib
```

Or install all dependencies at once:

```bash
pip install -r requirements.txt
```

## 💻 Usage

1. Clone the repository:
```bash
git clone https://github.com/yourusername/canny-edge-detection-camera.git
cd canny-edge-detection-camera
```

2. Run the application:
```bash
python canny_camera.py
```

3. Use keyboard controls to adjust the edge detection:

| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `+` | Increase high threshold (more edges) |
| `-` | Decrease high threshold (fewer edges) |
| `w` | Increase low threshold |
| `s` | Decrease low threshold |

## 🔧 How It Works

### The Canny Edge Detection Algorithm

The application implements the 5-step Canny edge detection process:

#### Step 1: Noise Reduction
```python
blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
```
Applies Gaussian blur to reduce noise and smooth the image.

#### Step 2: Gradient Calculation
```python
grad_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
grad_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
```
Uses Sobel operators to compute horizontal and vertical gradients.

#### Step 3: Non-Maximum Suppression
Thins the edges by keeping only local maxima in the gradient direction.

#### Step 4: Double Threshold
Classifies edge pixels into strong, weak, and non-edges using two threshold values.

#### Step 5: Edge Tracking by Hysteresis
Connects weak edges to strong edges to form complete edge contours.

## 📊 Parameters

- **Low Threshold** (default: 50): Minimum gradient magnitude for weak edges
- **High Threshold** (default: 150): Minimum gradient magnitude for strong edges
- **Kernel Size** (default: 5): Size of Gaussian blur kernel

## 📸 Screenshots

```
┌─────────────────────┬─────────────────────┐
│   ORIGINAL IMAGE    │    CANNY EDGES      │
│                     │                     │
│   [Camera Feed]     │   [Edge Detection]  │
│                     │                     │
└─────────────────────┴─────────────────────┘
       Low: 50 | High: 150
```

## 🎓 Academic Reference

This implementation is based on:
- **Course**: Image Processing (CSE281)
- **Lecture**: 7 - Boundary-based Segmentation
- **Instructor**: Dr. Mahmoud Zaki
- **Institution**: Faculty of Computer Engineering

## 📝 Code Structure

```
canny_camera.py
├── non_maximum_suppression()     # Step 3: Thin edges
├── double_threshold()            # Step 4: Classify edges
├── edge_tracking_by_hysteresis() # Step 5: Connect edges
├── canny_edge_detection()        # Complete algorithm
└── main()                        # Camera application
```

## 🐛 Troubleshooting

### Camera not opening?
- Make sure your camera is not being used by another application
- Try changing the camera index from `0` to `1` in `cv2.VideoCapture(0)`

### Slow performance?
- The algorithm processes each frame in real-time, which can be CPU-intensive
- Try reducing the camera resolution or frame rate

### Import errors?
- Ensure all dependencies are installed: `pip install -r requirements.txt`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dr. Mahmoud Zaki for the comprehensive lecture materials
- OpenCV community for the excellent computer vision library
- John Canny for developing the edge detection algorithm (1986)

## 📧 Contact

Your Name - [@yourhandle](https://twitter.com/yourhandle)

Project Link: [https://github.com/yourusername/canny-edge-detection-camera](https://github.com/yourusername/canny-edge-detection-camera)

---

⭐ If you found this project helpful, please give it a star!
