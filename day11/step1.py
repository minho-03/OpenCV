import cv2
import numpy as np
import os

# Cascade 분류기 로드 함수

def load_cascade(cascade_name='haarcascade_frontalface_default.xml'):

    """Haar Cascade 분류기 로드"""
    cascade_path = cv2.data.haarcascades + cascade_name
    cascade = cv2.CascadeClassifier(cascade_path)

    if cascade.empty():
        print(f"Error: {cascade_name} 로드 실패")
        return None
    return cascade

# 폴더 생성 함수
def create_folders(paths):
    """필요한 폴더 생성"""
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)

def apply_mosaic(frame, faces, block_size=5):
   
    for (x, y, w, h) in faces:
        face_roi = frame[y:y+h, x:x+w]
        small = cv2.resize(face_roi, (block_size, block_size))
        mosaic = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
        frame[y:y+h, x:x+w] = mosaic
    
    return frame

# Cascade 로드
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# 웹캠 시작
cap = cv2.VideoCapture(0)
print("웹캠 모자이크 처리 시작... (q로 종료)")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    # 모자이크 적용
    frame = apply_mosaic(frame, faces, block_size=15)
    cv2.imshow('Face Mosaic', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):

        break

cap.release()

cv2.destroyAllWindows()

