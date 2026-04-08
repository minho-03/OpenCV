import cv2
import numpy as np
import urllib.request
from sample_download import get_sample

# 방법 1: 강사 제공 샘플 이미지 사용

# img = cv2.imread(get_sample('messi5.jpg'))

# 방법 2: 인터넷에서 다운로드

# URL에서 이미지를 받아와 저장

url = "https://love.seoul.go.kr/tmda/Pds/Board/seoul_news_write/Editor/article_202104_09_01_04.jpg"

# 또는 다른 보행자 사진 URL 사용 가능

urllib.request.urlretrieve(url, 'pedestrian.jpg')

img = cv2.imread('pedestrian.jpg')

if img is None:

    print("Error: 이미지 로드 실패")

else:

    print(f"✅ 이미지 로드 성공: {img.shape}")

    cv2.imshow('Original', img)

    cv2.waitKey(0)

    cv2.destroyAllWindows()


# ① HOG 디스크립터 생성 ---

hog = cv2.HOGDescriptor()

# ② 사전학습된 보행자 검출 모델 로드 ---

hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

import time

class PedestrianDetectionStats:

    """보행자 감지 통계 수집"""

    

    def __init__(self):

        self.frame_count = 0

        self.detection_count = 0

        self.max_per_frame = 0

        self.detection_history = []

        self.start_time = time.time()

    

    def update(self, detections):

        """프레임 정보 업데이트"""

        self.frame_count += 1

        self.detection_count += len(detections)

        self.max_per_frame = max(self.max_per_frame, len(detections))

        self.detection_history.append(len(detections))

    

    def print_stats(self):

        """통계 출력"""

        elapsed = time.time() - self.start_time

        fps = self.frame_count / elapsed

        

        print("\n" + "="*50)

        print("📊 보행자 감지 통계")

        print("="*50)

        print(f"처리 시간: {elapsed:.1f}초")

        print(f"처리된 프레임: {self.frame_count}개")

        print(f"평균 FPS: {fps:.1f}")

        print(f"총 감지한 보행자: {self.detection_count}명")

        print(f"프레임당 평균: {self.detection_count/max(1, self.frame_count):.2f}명")

        print(f"최대 감지: {self.max_per_frame}명/프레임")

        

        # 감지되지 않은 프레임

        zero_detection = sum(1 for d in self.detection_history if d == 0)

        print(f"보행자 없는 프레임: {zero_detection}개 ({zero_detection/self.frame_count*100:.1f}%)")

# 사용

stats = PedestrianDetectionStats()

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:

    ret, frame = cap.read()

    if not ret:

        break

    

    detections, weights = hog.detectMultiScale(frame, winStride=(8, 8), padding=(16, 16), scale=1.05)

    filtered = [(x, y, w, h) for (x, y, w, h), w in zip(detections, weights) if w > 0.5]

    

    stats.update(filtered)

    

    for (x, y, w, h) in filtered:

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    

    cv2.imshow('Pedestrian Detection', frame)

    if cv2.waitKey(1) == 27:

        break

cap.release()

cv2.destroyAllWindows()

stats.print_stats()






