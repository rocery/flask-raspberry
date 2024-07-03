import cv2
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='USB Camera Test')
parser.add_argument('camera_index', type=int, help='Index of the camera to use')
args = parser.parse_args()

# Open the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print(f"Error: Could not open camera {args.camera_index}.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the resulting frame
    cv2.imshow('USB Camera Test', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()

# test add note

