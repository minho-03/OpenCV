# step1_color_detection_improved.py
import cv2 as cv
import numpy as np

def nothing(x):
    pass

cv.namedWindow('Trackbars')
cv.createTrackbar('H_Lower', 'Trackbars', 110, 179, nothing)
cv.createTrackbar('S_Lower', 'Trackbars', 50, 255, nothing)
cv.createTrackbar('V_Lower', 'Trackbars', 50, 255, nothing)
cv.createTrackbar('H_Upper', 'Trackbars', 121, 179, nothing)
cv.createTrackbar('S_Upper', 'Trackbars', 255, 255, nothing)
cv.createTrackbar('V_Upper', 'Trackbars', 255, 255, nothing)

AREA_THRESHOLD = 500
cap = cv.VideoCapture(0)

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    height, width = frame.shape[:2]
    
    roi_startY = int(height / 2)
    roi = frame[roi_startY:height, :] 
    
    hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
    
    h_l = cv.getTrackbarPos('H_Lower', 'Trackbars')
    s_l = cv.getTrackbarPos('S_Lower', 'Trackbars')
    v_l = cv.getTrackbarPos('V_Lower', 'Trackbars')
    h_u = cv.getTrackbarPos('H_Upper', 'Trackbars')
    s_u = cv.getTrackbarPos('S_Upper', 'Trackbars')
    v_u = cv.getTrackbarPos('V_Upper', 'Trackbars')
    
    lower_bound = np.array([h_l, s_l, v_l])
    upper_bound = np.array([h_u, s_u, v_u])
    
    mask = cv.inRange(hsv, lower_bound, upper_bound)
    mask_cleaned = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    
    area = cv.countNonZero(mask_cleaned)

    if area > AREA_THRESHOLD:
        status_text = f"DETECTED - open (Area: {area} px)"
        cv.rectangle(frame, (0, roi_startY), (width, height), (0, 255, 0), 2)
        cv.putText(frame, status_text, (10, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv.LINE_AA)
    else:
        status_text = "NOT DETECTED - closed"
        cv.rectangle(frame, (0, roi_startY), (width, height), (0, 0, 255), 2)
        cv.putText(frame, status_text, (10, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv.LINE_AA)
    # =========================================
        
    cv.imshow('Frame', frame)
    cv.imshow('Cleaned Mask', mask_cleaned)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()