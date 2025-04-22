import pygame
from djitellopy import Tello
import cv2
import time
import numpy as np
from collections import defaultdict

# Initialize pygame for capturing keyboard inputs
pygame.init()

# Create a Tello object
tello = Tello()

# Connect to the drone
tello.connect()

# Check battery status
print(f"Battery: {tello.get_battery()}%")

COLOR_RANGES = {
    "red": [((0, 120, 70), (10, 255, 255)), ((170, 120, 70), (180, 255, 255))],
    "orange": [((10, 100, 20), (25, 255, 255))],
    "yellow": [((25, 100, 100), (35, 255, 255))],
    "green": [((36, 50, 70), (89, 255, 255))],
    "blue": [((90, 50, 70), (128, 255, 255))],
    "purple": [((129, 50, 70), (158, 255, 255))]
}

# For cooldown (so it doesn't write every frame)
DETECTION_COOLDOWN = 5  # seconds
last_detected_time = defaultdict(lambda: 0)
color_detection_enabled = False
color_detection_start_time = None

# Start the video stream
tello.streamon()

# Create a window to detect key events
screen = pygame.display.set_mode((640, 480))  # Set a larger window size
pygame.display.set_caption("Tello Manual Control")

# Control variables
running = True
speed = 50

# Start controlling the drone
tello.takeoff()

# Main loop for controlling the drone with keyboard input and displaying the camera feed
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the camera feed
    frame = tello.get_frame_read().frame
    
    if frame is None:
        print("No frame available")
    else:
        # Resize the frame to fit in the Pygame window size
        frame_resized = cv2.resize(frame, (640, 480))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        hsv = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2HSV)
        current_time = time.time()

        if color_detection_enabled and color_detection_start_time and (time.time() - color_detection_start_time > 3):  # 3 seconds delay
            hsv = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2HSV)
            current_time = time.time()

            for color, ranges in COLOR_RANGES.items():
                mask_total = None

                for lower, upper in ranges:
                    lower_np = np.array(lower)
                    upper_np = np.array(upper)
                    mask = cv2.inRange(hsv, lower_np, upper_np)
                    mask_total = mask if mask_total is None else cv2.bitwise_or(mask_total, mask)

                pixels = cv2.countNonZero(mask_total)

                if pixels > 500 and (current_time - last_detected_time[color]) > DETECTION_COOLDOWN:
                    print(f"{color.capitalize()} detected!")

                    # Write to file without spamming
                    with open("detected_colors.txt", "a") as file:
                        file.write(f"{color}\n")

                    last_detected_time[color] = current_time

        for color, ranges in COLOR_RANGES.items():
            mask_total = None

            for lower, upper in ranges:
                lower_np = np.array(lower)
                upper_np = np.array(upper)
                mask = cv2.inRange(hsv, lower_np, upper_np)
                mask_total = mask if mask_total is None else cv2.bitwise_or(mask_total, mask)

            pixels = cv2.countNonZero(mask_total)

            if pixels > 500 and (current_time - last_detected_time[color]) > DETECTION_COOLDOWN:
                print(f"{color.capitalize()} detected!")

                # Write to file without spamming
                with open("detected_colors.txt", "a") as file:
                    file.write(f"{color}\n")

                last_detected_time[color] = current_time

        # Convert the frame to a surface for displaying with pygame
        frame_surface = pygame.surfarray.make_surface(frame_rgb)

        # Blit the frame onto the pygame screen
        frame_surface = pygame.transform.rotate(frame_surface, 270)
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()

    # Check for keyboard inputs for movement controls
    keys = pygame.key.get_pressed()

    # Forward and Backward Movement
    if keys[pygame.K_w]:
        tello.move_forward(speed)
    if keys[pygame.K_s]:
        tello.move_back(speed)

    # Left and Right Movement
    if keys[pygame.K_a]:
        tello.move_left(speed)
    if keys[pygame.K_d]:
        tello.move_right(speed)

    # Up and Down Movement
    if keys[pygame.K_e]:
        tello.move_up(30)
    if keys[pygame.K_q]:
        tello.move_down(30)

    # Rotation (Clockwise and Counterclockwise)
    if keys[pygame.K_LEFT]:
        tello.rotate_counter_clockwise(40)
    if keys[pygame.K_RIGHT]:
        tello.rotate_clockwise(40)

    #flips
    if keys[pygame.K_u]:
        tello.flip_forward()
    if keys[pygame.K_j]:
        tello.flip_back()
    if keys[pygame.K_h]:
        tello.flip_left()
    if keys[pygame.K_k]:
        tello.flip_right()

    # Emergency landing (press 'L' to land)
    if keys[pygame.K_l]:
        tello.land()
        
       # Exit the program (press 'ESC' to quit)
    if keys[pygame.K_ESCAPE]:
        running = False

# Land the drone before quitting
tello.land()

# End connection
tello.end()
pygame.quit()