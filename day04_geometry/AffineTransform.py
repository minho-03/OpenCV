import urllib.request
import os
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def get_sample(filename, repo='opencv'):
    """부교 또는 OpenCV 공식 샘플 이미지 자동 다운로드
    
    Args:
        filename (str): 이미지 파일명 (예: 'morphological.png')
        repo (str): 'insightbook' (부교) 또는 'opencv' (공식)
    
    Returns:
        str: 다운로드된 파일명
    """
    if not os.path.exists(filename):
        if repo == 'insightbook':
            url = f"https://raw.githubusercontent.com/dltpdn/insightbook.opencv_project_python/master/img/{filename}"
        else:  # opencv 공식
            url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return filename

# 사용 방법
# img = cv.imread(get_sample('morphological.png', repo='insightbook'))

img = cv.imread(get_sample('messi5.jpg'),cv.IMREAD_GRAYSCALE)
h,w = img.shape

# 3개의 점의 대응관계
pts1 = np.float32([[50,50],[200,50],[50,200]])
pts2 = np.float32([[10,100],[200,50],[100,250]])

# Affine 변환 행렬 계산
M = cv.getAffineTransform(pts1,pts2)
dst = cv.warpAffine(img,M,(w,h))

plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(dst),plt.title('Output')
plt.show()

cv.waitKey(0)
cv.destroyAllWindows()