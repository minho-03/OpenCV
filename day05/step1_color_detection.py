import numpy as np
import cv2 as cv

# 웹캠을 열기
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

# 감지할 색상의 HSV 범위 설정
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])

# 감지 면적 임계값 설정
AREA_THRESHOLD = 500

# 반복:
#   웹캠에서 프레임 읽기
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # HSV 색공간으로 변환
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # 마스크 생성 (특정 색상만 추출)
    mask = cv.inRange(hsv,lower_blue, upper_blue)

    # 마스크 픽셀 면적 계산
    area = cv.countNonZero(mask)

    # 면적과 임계값 비교하여 상태 결정 및 터미널 출력
    if area > AREA_THRESHOLD:
        print(f"DETECTED (Area: {area} px)")
    else:
        print(f"NOT DETECTED (Area: {area} px)")
        
    # 화면 표시
    cv.imshow('Original', frame)
    cv.imshow('Blue Mask', mask)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()