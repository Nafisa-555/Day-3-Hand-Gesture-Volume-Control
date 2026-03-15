# Hand Gesture Volume Control 🔊

This project is a Computer Vision application that allows users to control their system volume using hand gestures.

Using a webcam, the program detects the hand and measures the distance between the thumb and index finger to adjust the system volume in real time.

## Features

- Real-time hand tracking
- Volume control using finger gestures
- Smooth volume adjustment
- On-screen volume bar and percentage
- Webcam-based interaction

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- Pycaw (for system volume control)

## How It Works

The webcam captures live video using OpenCV.  
MediaPipe detects hand landmarks and tracks the thumb and index finger positions.

The distance between these two fingers is calculated and mapped to the system volume range.

As the distance increases, the volume increases, and when the fingers move closer, the volume decreases.


## Controls

Move thumb and index finger closer or farther apart to change the system volume.

Press **Q** to exit the program.


## Demo

Hand gesture controls the system volume in real time using webcam input.

## Author

Nafisa Ansari
