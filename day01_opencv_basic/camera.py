import numpy as np
import cv2 as cv

frame_count = 0
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    frame = cv.flip(frame, 1) # 카메라 반전
    cv.imshow('frame', frame)
    key = cv.waitKey(1)
    if key == ord('q'):
        break

    elif key == ord('c'):
        filename = f"./capture_{frame_count}.png"
        cv.imwrite(filename, frame)
        print(f"캡쳐 저장: {filename}")
        frame_count += 1

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()