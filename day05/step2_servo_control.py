import cv2 as cv
import numpy as np
import serial
import time

COM_PORT = 'COM4' 
try:
    arduino = serial.Serial(COM_PORT, 9600, timeout=1)
    time.sleep(2) 
    print("✅ PASS: 아두이노 연결 성공!")
except Exception as e:
    print(f"❌ FAIL: 아두이노 연결 실패 ({e})")
    arduino = None

lower_blue = np.array([110, 50, 50])
upper_blue = np.array([121, 255, 255])
AREA_THRESHOLD = 500

cap = cv.VideoCapture(0)

is_door_open = False 

while True:
    ret, frame = cap.read()
    if not ret: break
    
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    area = cv.countNonZero(mask)
    
    is_detected = area > AREA_THRESHOLD
    
    if is_detected and not is_door_open:
        print(f"파란색 감지됨 (Area: {area}) - OPEN")
        if arduino:
            arduino.write(b'O')
        is_door_open = True
        
    elif not is_detected and is_door_open:
        if arduino:
            arduino.write(b'C')
        is_door_open = False
        
    status_text = "DOOR: OPEN" if is_door_open else "DOOR: CLOSED"
    color = (0, 255, 0) if is_door_open else (0, 0, 255)
    cv.putText(frame, status_text, (10, 40), cv.FONT_HERSHEY_SIMPLEX, 1, color, 3)
    
    cv.imshow('Frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

if arduino:
    arduino.close()
cap.release()
cv.destroyAllWindows()