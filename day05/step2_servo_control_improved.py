import cv2 as cv
import numpy as np
import serial
import time

COM_PORT = 'COM4'
try:
    arduino = serial.Serial(COM_PORT, 9600, timeout=1)
    time.sleep(2)
    print("✅ 아두이노 연결 성공")
except Exception as e:
    print(f"❌ 아두이노 연결 실패")
    arduino = None

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

is_door_open = False
prev_frame_time = 0


extra_colors = {
    'Yellow': (np.array([20, 100, 100]), np.array([30, 255, 255]))
}

while True:
    process_start_time = time.time()
    
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
    
    mask_blue = cv.inRange(hsv, lower_bound, upper_bound)
    mask_blue_cleaned = cv.morphologyEx(mask_blue, cv.MORPH_OPEN, kernel)
    area_blue = cv.countNonZero(mask_blue_cleaned)
    
    detected_color = None
    max_area = 0
    
    if area_blue > AREA_THRESHOLD:
        detected_color = "Blue"
        max_area = area_blue
        
    for color_name, (lower, upper) in extra_colors.items():
        mask_extra = cv.inRange(hsv, lower, upper)
        mask_extra_cleaned = cv.morphologyEx(mask_extra, cv.MORPH_OPEN, kernel)
        area_extra = cv.countNonZero(mask_extra_cleaned)
        if area_extra > AREA_THRESHOLD and area_extra > max_area:
            detected_color = color_name
            max_area = area_extra

    if detected_color is not None:
        if not is_door_open:
            reaction_time = (time.time() - process_start_time) * 1000
            print(f"[{detected_color}] 감지됨 (반응속도: {reaction_time:.1f}ms)")
            if arduino: arduino.write(b'O')
            is_door_open = True
            
        status_text = f"DETECTED - open ({detected_color})"
        cv.rectangle(frame, (0, roi_startY), (width, height), (0, 255, 0), 2)
        cv.putText(frame, status_text, (10, 70), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv.LINE_AA)
        
    else:
        if is_door_open:
            reaction_time = (time.time() - process_start_time) * 1000
            print(f"(반응속도: {reaction_time:.1f}ms)")
            if arduino: arduino.write(b'C')
            is_door_open = False
            
        status_text = "NOT DETECTED - closed"
        cv.rectangle(frame, (0, roi_startY), (width, height), (0, 0, 255), 2)
        cv.putText(frame, status_text, (10, 70), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv.LINE_AA)
        
    current_time = time.time()
    fps = 1 / (current_time - prev_frame_time) if prev_frame_time > 0 else 0
    prev_frame_time = current_time
    cv.putText(frame, f"FPS: {int(fps)}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2, cv.LINE_AA)
        
    cv.imshow('Frame', frame)
    cv.imshow('Cleaned Mask (Blue)', mask_blue_cleaned)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

if arduino: arduino.close()
cap.release()
cv.destroyAllWindows()