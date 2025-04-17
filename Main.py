import pygame
from djitellopy import Tello
import cv2
import time

# Initialize pygame for capturing keyboard inputs
pygame.init()

# Create a Tello object
tello = Tello()

# Connect to the drone
tello.connect()

# Check battery status
print(f"Battery: {tello.get_battery()}%")

# Start the video stream
tello.streamon()

# Create a window to detect key events
screen = pygame.display.set_mode((640, 480))  # Set a larger window size
pygame.display.set_caption("Tello Manual Control")

# Control variables
running = True
speed = 50  # Speed level (0-100)

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
    
    if keys[pygame.K_SPACE]:
        # Capture and save the image
        timestamp = time.strftime("%Y%m%d-%H%M%S")  # Timestamp for uniqueness
        cv2.imwrite(f"tello_picture_{timestamp}.jpg", frame)
        print(f"Picture saved as tello_picture_{timestamp}.jpg")
        
    # Exit the program (press 'ESC' to quit)
    if keys[pygame.K_ESCAPE]:
        running = False

# Land the drone before quitting
tello.land()

# End connection
tello.end()
pygame.quit()