import cv2
import numpy as np

# Load image
image = cv2.imread('img10.jpg')

# Convert to HSV for color detection
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Convert to grayscale for circle detection
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Detect circles (LEDs)
circles = cv2.HoughCircles(
    blurred,
    cv2.HOUGH_GRADIENT,
    dp=1,
    minDist=15,
    param1=50,
    param2=20,
    minRadius=5,
    maxRadius=15
)

if circles is not None:
    circles = np.round(circles[0, :]).astype(int)
    led_colors = []

    for (x, y, r) in circles:
        # Extract ROI from HSV for color detection
        roi = hsv[y-r:y+r, x-r:x+r]
        if roi.size == 0:
            continue

        # Calculate average color
        avg_color = cv2.mean(roi)[:3]  # [H, S, V]
        hue = avg_color[0]
        saturation = avg_color[1]
        value = avg_color[2]

        # Classify color with intensity check for "Off"
        if value < 30 or saturation < 30:
            color = "Off"
        elif (hue >= 0 and hue <= 10) or (hue >= 160 and hue <= 180):
            color = "Red"
        elif hue >= 40 and hue <= 80:
            color = "Green"
        elif hue >= 100 and hue <= 140:
            color = "Blue"
        else:
            color = "Off"

        led_colors.append((x, y, color))
        cv2.circle(image, (x, y), r, (0, 255, 0), 2)  # Draw detected circle

    # Ensure 64 LEDs by filling missing spots (if any)
    led_colors.sort(key=lambda x: (x[1], x[0]))  # Sort by y, then x
    while len(led_colors) < 64:
        led_colors.append((0, 0, "Off"))  # Pad with "Off" if not enough detected

    # Map to 8x8 grid
    grid = [led_colors[i:i+8] for i in range(0, 64, 8)]  # 8x8 grid

    # Print grid
    for row in grid:
        print([led[2] for led in row])

    # Resize image for better viewing
    output_image = cv2.resize(image, (400, 400))  # Resize to 400x400 pixels
    cv2.imwrite("output_resized.jpg", output_image)
