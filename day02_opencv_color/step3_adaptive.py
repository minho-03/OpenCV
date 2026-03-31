import cv2 as cv
import numpy as np

# 이미지 읽기 (그레이스케일)
import urllib.request
import os

def get_sample(filename):
    if not os.path.exists(filename):
        url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return filename
# — 조명 불균형이 있는 이미지 권장
img_path = get_sample("sudoku.png")
img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)

# 콜백 함수
def nothing(x):
    pass

# 창 생성
cv.namedWindow('image')

# 트랙바 생성
# — blockSize (3~31, 초기값 11, 반드시 홀수)
# — C (0~20, 초기값 2)
cv.createTrackbar('blockSize','image',11,31,nothing)
cv.createTrackbar('C','image',2,20,nothing)

# 반복문
while True:
    # 트랙바 값 읽기
    blockSize = cv.getTrackbarPos('blockSize','image')
    c = cv.getTrackbarPos('C','image')

    # blockSize가 짝수면 1 더하기 (홀수 보장)
    # — if blockSize % 2 == 0: blockSize += 1
    if blockSize < 3:
        blockSize = 3
    if blockSize % 2 == 0:
        blockSize += 1

    # Global Threshold (고정)
    # — cv.threshold(img, 127, 255, cv.THRESH_BINARY)
    _, global_th = cv.threshold(img, 127, 255, cv.THRESH_BINARY)

    # Otsu 자동 이진화
    # — cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    _, otsu_th = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # Adaptive Mean Threshold
    # — cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C,
    #                        cv.THRESH_BINARY, blockSize, C)
    mean_th = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, blockSize, c)

    # Adaptive Gaussian Threshold
    # — cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                        cv.THRESH_BINARY, blockSize, C)
    gaussian_th = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, blockSize, c)

    # 2x2 격자로 표시
    # — top = np.hstack([global_th, otsu_th])
    # — bottom = np.hstack([mean_th, gaussian_th])
    # — result = np.vstack([top, bottom])
    top = np.hstack([global_th, otsu_th])
    bottom = np.hstack([mean_th, gaussian_th])
    result = np.vstack([top, bottom])

    cv.imshow('image', result)

    # 'q' → 종료
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# 창 닫기
cv.destroyAllWindows()