# H.O.V.E.R (Hand Operated Virtual External Remote) - Silicon Sorcerers

**Team Members:** Mohan Gowda T, Naga Balaji K N, Nithu Shree, Indhu Shriya

## Project Overview

H.O.V.E.R is an innovative AI-driven solution that transforms hand gestures into mouse movements and controls. By utilizing a webcam, the system tracks hand landmarks to perform various computer operations such as mouse movement, clicking, and keyboard key presses. This project leverages the power of Mediapipe for hand tracking, OpenCV for image processing, and Autopy for controlling the mouse and keyboard.

## Key Features

- **Hand Gesture Recognition:** Utilizes Mediapipe to detect and track hand landmarks in real-time.
- **Mouse Movement:** Converts hand movements into mouse cursor movements on the screen.
- **Gesture-Based Controls:** Implement specific gestures for different actions like clicking, scrolling, and keyboard key presses.
- **Real-Time Performance:** Ensures smooth and responsive hand gesture detection and mouse control.
- **Cross-Platform Compatibility:** Compatible with different operating systems that support Python and the required libraries.

## Installation

### Prerequisites

- Python 3.8.2
- Webcam

### Supported Python Libraries

To run this project, you need to install the following libraries:

```sh
pip install mediapipe==0.10.1
pip install opencv-python==4.7.0.72
pip install autopy==4.0.0
pip install numpy==1.24.3
```

### Setup Instructions

1. **Clone the Repository:**

```sh
git clone https://github.com/your-repository/HOVER.git
cd HOVER
```

2. **Install Dependencies:**

Ensure you have Python 3.8.2 installed. Then, run:

```sh
pip install mediapipe==0.10.1
pip install opencv-python==4.7.0.72
pip install autopy==4.0.0
pip install numpy==1.24.3
```

3. **Run the Application:**

```sh
python hover.py
```

## Usage

1. **Start the Application:**

Run the Python script to start the webcam and initiate hand tracking.

2. **Perform Gestures:**

   - **Mouse Movement:** Move your hand to control the mouse cursor.
   - **Click:** Use specific gestures like the thumb up for left-click.
   - **Keyboard Controls:** Perform gestures to simulate key presses (e.g., spacebar, arrow keys).

3. **Exit the Application:**

Press 'q' to quit the application.

## How It Works

- **Hand Landmarks Detection:** Uses Mediapipe to detect and track hand landmarks.
- **Gesture Interpretation:** Analyzes the position of fingers to determine specific gestures.
- **Mouse and Keyboard Control:** Uses Autopy to move the mouse cursor and perform keyboard actions based on the detected gestures.

## Future Enhancements

1. **Multi-Hand Support:** Extend the functionality to support and track multiple hands simultaneously.
2. **Custom Gestures:** Allow users to define and train custom gestures for specific actions.
3. **Enhanced Accuracy:** Improve the accuracy of hand landmark detection and gesture recognition.
4. **Voice Integration:** Integrate voice commands for additional control options.
5. **Settings UI:** Develop a graphical user interface to customize settings and calibrate hand movements.

## Contributing

We welcome contributions to enhance H.O.V.E.R. Please fork the repository, create a feature branch, and submit a pull request with your improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
