import urllib.request
import os
import numpy as np
import cv2 as cv

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

# 회전이동 (중심점, 각도, 스케일)
M = cv.getRotationMatrix2D(((w-1)/2.0,(h-1)/2.0),90,1)
dst = cv.warpAffine(img,M,(w,h))


cv.imshow('original',img)
cv.imshow('Rotated',dst)
cv.waitKey(0)
cv.destroyAllWindows()