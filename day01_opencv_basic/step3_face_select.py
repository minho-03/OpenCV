import cv2 as cv
import numpy as np

# my_id_card.png 읽기
img = cv.imread('my_id_card.png')

# 이미지를 불러오지 못한 경우 예외 처리
if img is None:
    print("이미지를 불러올 수 없습니다. 파일명을 확인하세요.")
    exit()

# 원본 복사본 만들기 — 드래그 중 이전 사각형을 지우기 위해
# (주석의 흐름에 맞춰 여기서 초기 복사본을 만듭니다.)
img_orig = img.copy()

# 전역 변수: ix, iy (시작점), drawing (드래그 중 여부)
ix, iy = -1, -1
drawing = False

# 마우스 콜백 함수 정의
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, img, img_orig

    # LBUTTONDOWN: 드래그 시작, 시작점(ix, iy) 저장
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    # MOUSEMOVE: 드래그 중이면
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            # 원본에서 img 복원 (이전 사각형 제거)
            img = img_orig.copy()
            # 현재 위치까지 초록색 사각형 그리기 (두께 2)
            cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)

    # LBUTTONUP: 드래그 끝
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        # 최종 사각형 그리기
        cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
        # 사각형 위에 "FACE" 텍스트 넣기
        # (시작점 ix, iy 기준으로 약간 위쪽에 텍스트 배치)
        font = cv.FONT_HERSHEY_SIMPLEX
        text_pos = (ix, iy - 10 if iy - 10 > 10 else iy + 20) # 글자가 화면 밖으로 나가지 않게 처리
        cv.putText(img, "FACE", text_pos, font, 0.6, (0, 255, 0), 2, cv.LINE_AA)

# 창 생성 + 마우스 콜백 등록
cv.namedWindow('image')
cv.setMouseCallback('image', draw_rectangle)

# 반복문
while(1):
    # 이미지 표시
    cv.imshow('image', img)
    
    # 키 입력 대기
    k = cv.waitKey(1) & 0xFF
    
    # 's' → my_id_card_final.png로 저장 후 break
    if k == ord('s'):
        cv.imwrite('my_id_card_final.png', img)
        print("최종 이미지가 저장되었습니다: my_id_card_final.png")
        break
    # 'q' → break
    elif k == ord('q'):
        break

# 창 닫기
cv.destroyAllWindows()