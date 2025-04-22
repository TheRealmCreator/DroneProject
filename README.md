# DroneProject
This project allows you to control a DJI Tello drone using a keyboard, while also detecting specific colors in the live camera feed. When a color is detected, the program logs the detected color to a file. The system also enables you to toggle color detection on and off with a keybind.

Features:

Manual drone control with the keyboard.

Color detection for specific colors in the camera feed (e.g., red, green, blue).

Logs detected colors to a text file, avoiding repeated detections in a short time.

Supports toggling color detection with a keybind.

Why it was built:

To provide a flexible and easy-to-use interface for controlling the Tello drone.

To implement color detection and tracking capabilities for the drone, useful for various applications like object tracking, obstacle detection, and more.

HOW TO INSTALL:
Prerequisites
Before running the program, ensure you have the following:

Python 3.6+ installed

Pygame for handling keyboard input

OpenCV for video capture and processing

djitellopy for interfacing with the Tello drone

Install Dependencies
To install the required libraries, run the following in your terminal or command prompt:

pip install pygame opencv-python djitellopy numpy
How to install the project
Clone the repository or download the files to your local machine.

Ensure the Tello drone is connected to your WiFi network.

Run the script using Python:
python tello_color_detection.py




Controls:

Arrow keys (Left/Right): Rotate the drone.

W: Move forward.

S: Move backward.

A: Move left.

D: Move right.

E: Move up.

Q: Move down.

U: Flip forward.

J: Flip backward.

H: Flip left.

K: Flip right.

L: Emergency landing.

Esc: Quit the program.





If you'd like to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request. Contributions can include bug fixes, new features (such as more color detection options), or improvements to the user interface.

Steps for contributing:
Fork the repository.

Clone your fork:

bash
Copy
Edit
git clone <your-fork-url>
Create a new branch:

bash
Copy
Edit
git checkout -b feature/your-feature-name
Make your changes.

Commit your changes:

git commit -m "Your commit message"
Push your changes:


git push origin feature/your-feature-name
Submit a pull request to the main repository.
