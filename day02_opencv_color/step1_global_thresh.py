import cv2 as cv
import numpy as np
import urllib.request
import os

# 이미지 읽기 (그레이스케일)
# — cv.imread('image.png', cv.IMREAD_GRAYSCALE)
# — 또는 노이즈 제거: cv.medianBlur(img, 5)
def download_sample(filename):
    if not os.path.exists(filename):
        url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return filename

img = cv.imread(download_sample("sudoku.png"), cv.IMREAD_GRAYSCALE)
img = cv.medianBlur(img, 5)
# 콜백 함수 (트랙바용 — 빈 함수)
def nothing(x):
    pass

# 창 생성 (namedWindow)
cv.namedWindow('image')
# 트랙바 생성
# — threshold (0~255, 초기값 127)
# — mode: 0=THRESH_BINARY, 1=THRESH_BINARY_INV
cv.createTrackbar('s','image',127,255,nothing)
cv.createTrackbar('mode','image',0,1,nothing)

# 반복문
while True:
    # 트랙바 값 읽기 (getTrackbarPos)
    thresh_val = cv.getTrackbarPos('s','image')
    mode_val = cv.getTrackbarPos('mode','image')
    
    # 이진화 적용
    # — mode가 0이면 THRESH_BINARY, 1이면 THRESH_BINARY_INV
    if mode_val == 0:
        ret, thresh = cv.threshold(img, thresh_val, 255, cv.THRESH_BINARY)
    else:
        ret, thresh = cv.threshold(img, thresh_val, 255, cv.THRESH_BINARY_INV)

    # 원본 | 이진화 결과 나란히 표시
    # — np.hstack([img, thresh]) 또는 np.hstack([img, result])
    result = np.hstack([img,thresh])

    # 현재 임계값을 화면에 표시
    # — cv.putText(result, f'Thresh: {value}', ...)
    cv.putText(result, f'Thresh: {thresh_val} / Mode: {mode_val}', (10, 40), cv.FONT_HERSHEY_SIMPLEX, 1, 255, 2)

    cv.imshow('image',result)
    # 'q' → 종료
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# 창 닫기
cv.destroyAllWindows()