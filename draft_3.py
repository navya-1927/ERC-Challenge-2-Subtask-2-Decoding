import cv2
import numpy as np

# Load image
image = cv2.imread('img3.jpg')

# Convert to HSV for brightness detection
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Use Value channel to detect bright regions
value = hsv[:, :, 2]
_, thresh = cv2.threshold(value, 90, 255, cv2.THRESH_BINARY)  # Adjust 50 based on brightness

# Apply morphological closing to connect LEDs into a single region
kernel = np.ones((15, 15), np.uint8)  # Adjust kernel size to connect LEDs
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Find contours
contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if not contours:
    print("No contours found.")
    exit()

# Get the largest contour (assuming it's the matrix)
largest_contour = max(contours, key=cv2.contourArea)

# Get the bounding rectangle
x, y, w, h = cv2.boundingRect(largest_contour)

# Isolate the matrix region
matrix_roi = image[y:y+h, x:x+w]

# Subdivide into 8x8 grid (64 squares)
cell_width = w // 8
cell_height = h // 8
grid = []
for i in range(8):
    row = []
    for j in range(8):
        # Extract each cell, ensuring it fits within the ROI
        start_x = j * cell_width
        start_y = i * cell_height
        end_x = min(start_x + cell_width, w)
        end_y = min(start_y + cell_height, h)
        cell = matrix_roi[start_y:end_y, start_x:end_x]
        if cell.size == 0:
            row.append("Off")
            continue

        # Convert to HSV for color detection
        hsv_cell = cv2.cvtColor(cell, cv2.COLOR_BGR2HSV)
        avg_color = cv2.mean(hsv_cell)[:3]  # [H, S, V]
        hue = avg_color[0]
        saturation = avg_color[1]
        value = avg_color[2]

        # Classify color with intensity check
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

        row.append(color)
    grid.append(row)

# Print the 8x8 grid
for row in grid:
    print(row)

# Draw the bounding box and grid on the original image for visualization
cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
for i in range(9):  # 9 lines for 8x8 grid
    cv2.line(image, (x, y + i * cell_height), (x + w, y + i * cell_height), (0, 255, 0), 1)
    cv2.line(image, (x + i * cell_width, y), (x + i * cell_width, y + h), (0, 255, 0), 1)

# Resize for better viewing
output_image = cv2.resize(image, (600, 600))  # Adjust size as needed

# Display result
cv2.imshow('Detected Grid', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
