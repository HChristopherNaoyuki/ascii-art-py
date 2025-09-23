import cv2
import os
import time
import numpy as np
import sys

def precompute_ascii_mapping():
    """
    Precompute ASCII character mapping for all possible pixel values (0-255)
    This avoids repeated calculations during frame processing
    """
    ascii_chars = " .:-=+*#%@"
    mapping = []
    
    # Create a lookup table for all 256 possible grayscale values
    for pixel_value in range(256):
        # Normalize pixel value and map to ASCII character
        normalized = pixel_value / 255.0
        index = int(normalized * (len(ascii_chars) - 1))
        mapping.append(ascii_chars[index])
    
    return mapping

# Precompute the mapping once at module load
ASCII_MAPPING = precompute_ascii_mapping()

def convert_frame_to_ascii_optimized(frame, width=80):
    """
    Optimized frame to ASCII conversion using precomputed mapping and numpy operations
    """
    # Calculate height maintaining aspect ratio (terminal characters are taller than wide)
    height = max(1, int(frame.shape[0] * width / frame.shape[1] / 2))
    
    # Resize frame to target dimensions using area interpolation for better quality
    resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
    
    # Convert to grayscale if needed
    if len(resized_frame.shape) > 2:
        gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    else:
        gray_frame = resized_frame
    
    # Flatten the 2D array and use vectorized lookup
    flat_gray = gray_frame.flatten()
    
    # Use numpy to efficiently map all pixels to ASCII characters
    ascii_array = np.array([ASCII_MAPPING[pixel] for pixel in flat_gray], dtype='U1')
    
    # Reshape back to 2D and join with newlines
    ascii_array_2d = ascii_array.reshape(height, width)
    ascii_frame = '\n'.join(''.join(row) for row in ascii_array_2d)
    
    return ascii_frame

def get_terminal_size():
    """
    Get current terminal dimensions for automatic sizing
    """
    try:
        # Try to get terminal size using os.get_terminal_size (Python 3.3+)
        size = os.get_terminal_size()
        return size.columns, size.lines
    except (AttributeError, OSError):
        # Fallback to environment variables or default size
        try:
            cols = int(os.environ.get('COLUMNS', 80))
            rows = int(os.environ.get('LINES', 24))
            return cols, rows
        except (ValueError, TypeError):
            return 80, 24

def clear_terminal():
    """
    Efficient terminal clearing using ANSI escape sequences
    """
    # ANSI escape code for clear screen and cursor home
    sys.stdout.write('\033[2J\033[H')
    sys.stdout.flush()

def play_video_in_terminal_optimized(video_path, width=None, fps=None):
    """
    Optimized video playback in terminal with better performance and error handling
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return False
    
    # Get terminal size if width not specified
    if width is None:
        terminal_width, terminal_height = get_terminal_size()
        # Reserve one line for potential status info
        width = min(terminal_width, 200)  # Cap width for performance
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_path}'")
        return False
    
    # Get video properties
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Use provided FPS or video FPS, with sensible defaults
    target_fps = fps or video_fps or 30
    frame_delay = 1.0 / target_fps
    
    print(f"Playing: {os.path.basename(video_path)}")
    print(f"Resolution: {width} chars, FPS: {target_fps:.1f}")
    print("Press Ctrl+C to stop...")
    time.sleep(1.5)  # Brief pause to let user read info
    
    frame_count = 0
    start_time = time.time()
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert frame to ASCII
            ascii_art = convert_frame_to_ascii_optimized(frame, width)
            
            # Clear terminal efficiently
            clear_terminal()
            
            # Print ASCII art
            print(ascii_art)
            
            # Calculate and maintain target FPS
            frame_count += 1
            elapsed_time = time.time() - start_time
            expected_time = frame_count * frame_delay
            
            # Sleep only if we're ahead of schedule
            if elapsed_time < expected_time:
                time.sleep(expected_time - elapsed_time)
            else:
                # If we're behind, don't sleep to catch up
                pass
                
    except KeyboardInterrupt:
        print("\n\nVideo playback interrupted by user.")
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
    finally:
        # Calculate and display performance stats
        total_time = time.time() - start_time
        actual_fps = frame_count / total_time if total_time > 0 else 0
        
        print(f"\nPlayback completed:")
        print(f"Frames processed: {frame_count}")
        print(f"Actual FPS: {actual_fps:.1f}")
        
        cap.release()
        return True

def main():
    """
    Main function with improved user interaction
    """
    print("=== Terminal Video Player ===")
    
    # Get video path with validation
    while True:
        video_path = input("Enter the path to the video file: ").strip()
        if os.path.exists(video_path):
            break
        print("File not found. Please try again.")
    
    # Get terminal width with validation
    try:
        terminal_width, _ = get_terminal_size()
        width_input = input(f"Enter terminal width (default: {terminal_width}, max: 200): ").strip()
        width = int(width_input) if width_input else terminal_width
        width = max(40, min(width, 200))  # Clamp between 40 and 200
    except ValueError:
        width = terminal_width
    
    # Get FPS with validation
    try:
        fps_input = input("Enter target FPS (default: use video FPS): ").strip()
        fps = int(fps_input) if fps_input else None
        if fps and fps <= 0:
            fps = None
    except ValueError:
        fps = None
    
    print("\nStarting playback...")
    success = play_video_in_terminal_optimized(video_path, width, fps)
    
    if success:
        print("Thank you for using Terminal Video Player!")

if __name__ == "__main__":
    main()