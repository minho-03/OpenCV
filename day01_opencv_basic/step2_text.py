import cv2 as cv
import numpy as np

# 1. my_photo.png 읽기
# (파일이 같은 폴더에 있어야 합니다. 없으면 경로를 수정하세요)
img = cv.imread('my_photo.png')

if img is None:
    print("이미지를 불러올 수 없습니다. 파일명을 확인하세요.")
else:
    # 2. 이미지 높이(h), 너비(w) 가져오기
    h, w = img.shape[:2]

    # --- 하단 반투명 배경 바 ---
    # 1) 원본 복사본 만들기 (합성용 레이어)
    overlay = img.copy()

    # 2) overlay 하단 80px 영역에 검정 사각형 채우기 (두께 -1)
    cv.rectangle(overlay, (0, h - 80), (w, h), (0, 0, 0), -1)

    # 3) addWeighted로 img와 overlay를 50:50 합성
    img_result = cv.addWeighted(overlay, 0.5, img, 0.5, 0,img)

    # --- 텍스트 ---
    font = cv.FONT_HERSHEY_SIMPLEX
    
    # 이름 텍스트
    name_text = "NAME: PARK MIN HO"
    cv.putText(img_result, name_text, (20, h - 50), font, 0.8, (255, 255, 255), 2, cv.LINE_AA)

    # 소속 텍스트
    group_text = "GROUP: YH"
    cv.putText(img_result, group_text, (20, h - 20), font, 0.5, (200, 200, 200), 1, cv.LINE_AA)

    # 4. 결과 표시
    cv.imshow('Final ID Card', img_result)

    # 5. 키 입력 대기
    cv.waitKey(0)

    # 6. my_id_card.png로 저장
    cv.imwrite('my_id_card.png', img_result)
    print("성공적으로 저장되었습니다!!")

# 7. 창 닫기
cv.destroyAllWindows()