import cv2 as cv
import numpy as np

# 이미지 읽기 (그레이스케일)
import urllib.request
import os

def get_sample(filename):
    if not os.path.exists(filename):
        url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return cv.imread(filename)

def nothing(x):
    pass

# 파일 읽기
#img = cv.imread("./samples/starry_night.jpg")
#img = get_sample("starry_night.jpg")
img = get_sample("sudoku.png")
img = cv.imread('sudoku.png', cv.IMREAD_GRAYSCALE)
# 창 생성
cv.namedWindow("image")
# 트랙바 생성
# — manual_thresh (0~255, 초기값 127) — 수동 이진화용
# — mode: 0=Otsu만, 1=수동+ Otsu 비교
cv.createTrackbar('manual_thresh','image',127,255, nothing)
cv.createTrackbar('mode','image',0,1,nothing)


# 반복문
while True:
    manual_thresh = cv.getTrackbarPos('manual_thresh', 'image')
    mode = cv.getTrackbarPos('mode', 'image')
    # 수동 이진화
    # — cv.threshold(img, manual_thresh, 255, cv.THRESH_BINARY)
    _, manual_th = cv.threshold(img, manual_thresh, 255, cv.THRESH_BINARY)

    # Otsu 자동 이진화
    # — cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # — 반환값 중 ret이 실제 계산된 임계값
    ret_otsu, otsu_th = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # 2개 또는 3개 비교 표시
    # — mode가 0이면: 원본 | 수동 | Otsu
    # — mode가 1이면: 원본 | 수동 | Otsu
    if mode == 0:
        result = np.hstack([img, otsu_th])
    else:
        result = np.hstack([img, manual_th, otsu_th])

    # Otsu 임계값을 화면에 표시
    # — cv.putText(otsu_th, f'Otsu: {ret_otsu:.0f}', ...)
    cv.putText(result, f'Otsu: {ret_otsu:.0f}', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, 255, 2)

    cv.imshow('image',result)

    # 'q' → 종료
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# 창 닫기
cv.destroyAllWindows()