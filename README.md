# Terminal Video Player

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Installation and Setup](#installation-and-setup)
5. [Features](#features)
6. [Model Implementation](#model-implementation)
7. [Controller Implementation](#controller-implementation)
8. [View Implementation](#view-implementation)
9. [Styling and Design](#styling-and-design)
10. [Running the Application](#running-the-application)
11. [Disclaimer](#disclaimer)

## Project Overview

The **Terminal Video Player** is a Python-based application 
that allows users to watch video files directly in the terminal 
as ASCII art. The program optimizes video playback by leveraging 
efficient frame conversion to ASCII and handling terminal resizing. 
Users can customize video display settings such as terminal width 
and frames per second (FPS), while the application automatically 
adjusts for different terminal sizes.

## Technology Stack

* **Python**: The core language for the application.
* **OpenCV**: Used for video file handling and frame processing.
* **NumPy**: Utilized for optimized ASCII frame conversion.
* **OS Module**: Handles terminal-related operations like resizing and clearing the screen.

## Project Structure

```
/terminal_video_player
├── ascii_art_py.py
└── README.md
```

## Installation and Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/HChristopherNaoyuki/ascii-art-py.git
   cd ascii-art-py
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:

   ```bash
   python ascii_art_py.py
   ```

Make sure you have the necessary permissions and that OpenCV is properly installed.

## Features

* **Optimized Video Playback**: Efficient frame conversion to ASCII using precomputed mappings and NumPy vectorization.
* **Terminal Sizing**: Automatically detects terminal size, with options to customize width and height.
* **Error Handling**: Comprehensive error messages for missing files or incorrect inputs.
* **Custom FPS**: Users can define the target FPS for smooth video playback.
* **Interactive Interface**: Prompts users for file selection and configuration settings.

## Model Implementation

The model, responsible for converting video frames into ASCII characters, 
uses a precomputed lookup table that maps pixel values (0-255) to ASCII 
characters based on brightness levels. This method avoids recalculating 
the mappings during each frame processing, thus improving performance.

```python
def precompute_ascii_mapping():
    ascii_chars = " .:-=+*#%@"
    mapping = []
    for pixel_value in range(256):
        normalized = pixel_value / 255.0
        index = int(normalized * (len(ascii_chars) - 1))
        mapping.append(ascii_chars[index])
    return mapping
```

The frame-to-ASCII conversion is done through efficient NumPy operations to convert the frame into grayscale and then map it to ASCII characters.

## Controller Implementation

The controller is responsible for managing video playback and user interactions. The `play_video_in_terminal_optimized` function orchestrates the reading of the video, frame conversion, terminal clearing, and display.

```python
def play_video_in_terminal_optimized(video_path, width=None, fps=None):
    # Opens the video file and processes each frame
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_path}'")
        return False
    
    # Processes frames and prints ASCII art to terminal
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ascii_art = convert_frame_to_ascii_optimized(frame, width)
        clear_terminal()
        print(ascii_art)
    cap.release()
    return True
```

## View Implementation

The view is responsible for presenting the ASCII video frames in the terminal. 
The `clear_terminal` function ensures the screen is cleared before each new frame is rendered, creating a smoother playback experience.

```python
def clear_terminal():
    sys.stdout.write('\033[2J\033[H')
    sys.stdout.flush()
```

## Styling and Design

The design of the application is minimalistic, with a focus on performance and simplicity. The ASCII art uses a set of characters arranged by brightness:

```
" .:-=+*#%@"
```

This allows for a visually appealing representation of video content using only characters in the terminal.

## Running the Application

To run the application, follow these steps:

1. Clone the repository and install the dependencies as described above.
2. Use the following command to run the application:

   ```bash
   python ascii_art_py.py
   ```
3. The application will prompt you to enter the path of a video file. Once provided, it will begin processing and displaying the video in ASCII art.

You can customize the terminal width and FPS during the setup process.

## Disclaimer

The video playback in the terminal is limited by the capabilities of your terminal emulator. 
The video quality will be significantly lower than traditional video players, as it uses ASCII 
characters to represent images. Additionally, the performance may vary depending on the system's 
hardware and the terminal's size.

---
