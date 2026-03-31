import cv2 as cv
import numpy as np

# 웹캠 연결
# — cap = cv.VideoCapture(0)
# — cap.isOpened()로 연결 확인
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("웹캠을 열 수 없습니다. 카메라 연결을 확인해주세요.")
    exit()

# 콜백 함수
def nothing(x):
    pass

# 창 생성
cv.namedWindow('Webcam Thresholding')

# 트랙바 생성
# — blockSize (3~31, 초기값 11)
# — C (0~20, 초기값 2)
cv.createTrackbar('blockSize', 'Webcam Thresholding', 11, 31, nothing)
cv.createTrackbar('C', 'Webcam Thresholding', 2, 20, nothing)

# 반복문
while True:
    # 프레임 읽기
    # — ret, frame = cap.read()
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다. 프로그램을 종료합니다.")
        break

    # 그레이스케일 변환
    # — gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # blur (선택사항 — 웹캠 노이즈 감소)
    # — gray = cv.medianBlur(gray, 5)
    gray = cv.medianBlur(gray, 5)

    # blockSize 홀수 보장
    blockSize = cv.getTrackbarPos('blockSize', 'Webcam Thresholding')
    C = cv.getTrackbarPos('C', 'Webcam Thresholding')
    
    if blockSize < 3:
        blockSize = 3
    if blockSize % 2 == 0:
        blockSize += 1

    # 이진화 4종 비교 (Global / Otsu / Mean / Gaussian)
    _, global_th = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
    _, otsu_th = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    mean_th = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, blockSize, C)
    gaussian_th = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, blockSize, C)

    # 결과 표시
    top = np.hstack([global_th, otsu_th])
    bottom = np.hstack([mean_th, gaussian_th])
    result = np.vstack([top, bottom])
    
    cv.imshow('Webcam Thresholding', result)

    # 'q' → 종료
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# 카메라 해제 + 창 닫기
cap.release()
cv.destroyAllWindows()