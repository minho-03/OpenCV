#얼굴 왜곡import cv2
import dlib
import numpy as np
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


# 1. Dlib 얼굴 인식기 및 68-랜드마크 예측기 로드
detector = dlib.get_frontal_face_detector()
# dat 파일이 같은 경로에 있어야 합니다!
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 웹캠 켜기
cap = cv2.VideoCapture(0)

print("Delaunay 삼각망 실습 시작! (종료하려면 'q'를 누르세요)")

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 얼굴 찾기
    faces = detector(gray)
    
    for face in faces:
        # 1. 68개 랜드마크 추출
        landmarks = predictor(gray, face)
        points = []
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            points.append((x, y))
            # (선택) 랜드마크 점 찍기
            cv2.circle(frame, (x, y), 2, (0, 255, 255), -1)

        # 2. Delaunay 삼각분할을 위한 Subdiv2D 객체 생성
        # 얼굴을 감싸는 사각형 영역을 먼저 정의합니다.
        rect = (0, 0, frame.shape[1], frame.shape[0])
        subdiv = cv2.Subdiv2D(rect)
        
        # 추출한 68개 점을 Subdiv2D에 집어넣기
        for p in points:
            subdiv.insert(p)
            
        # 3. 삼각분할 데이터(삼각형 3개의 꼭짓점 좌표들) 가져오기
        triangleList = subdiv.getTriangleList()
        
        # 4. 화면에 삼각형 그물망(Mesh) 그리기
        for t in triangleList:
            # 삼각형의 3 꼭짓점 (x, y) 좌표 추출
            pt1 = (int(t[0]), int(t[1]))
            pt2 = (int(t[2]), int(t[3]))
            pt3 = (int(t[4]), int(t[5]))
            
            # 얼굴 영역(화면 크기)을 벗어나는 삼각형은 그리지 않음
            if (pt1[0] < 0 or pt1[0] > rect[2] or pt1[1] < 0 or pt1[1] > rect[3] or
                pt2[0] < 0 or pt2[0] > rect[2] or pt2[1] < 0 or pt2[1] > rect[3] or
                pt3[0] < 0 or pt3[0] > rect[2] or pt3[1] < 0 or pt3[1] > rect[3]):
                continue
                
            # 삼각형 선 그리기
            cv2.line(frame, pt1, pt2, (255, 0, 0), 1)
            cv2.line(frame, pt2, pt3, (255, 0, 0), 1)
            cv2.line(frame, pt3, pt1, (255, 0, 0), 1)

    cv2.imshow("Delaunay Triangulation", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()