import cv2 as cv
import numpy as np

def detect_color(frame):
    return False

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("❌ 웹캠을 열 수 없습니다.")
    exit()

ret,frame = cap.read()
if not ret:
    print("❌ 프레임을 읽을 수 없습니다.")
    cap.release()
    exit()

result = detect_color(frame)

if result:
    print("✅ PASS: 색상 감지 성공!")
else:
    print("❌ FAIL: detect_color() 함수가 아직 구현되지 않았습니다.")

cap.release()