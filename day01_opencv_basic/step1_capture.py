import cv2 as cv

# 웹캠 연결
frame_count = 0
cap = cv.VideoCapture(0)
# 카메라가 열리지 않으면 에러 메시지 출력 후 종료
if not cap.isOpened():
    print("Cannot open camera")
    exit()
# 반복문
    # 프레임 읽기
    # 읽기 실패 시 break
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # 좌우 반전
    frame = cv.flip(frame, 1)
    # 프레임 표시
    cv.imshow('frame',frame)
    # 키 입력 대기 (한 번만 호출)
    # 'c' → my_photo.png로 저장 + "캡쳐 완료!" 출력 후 break
    # 'q' → break
    key = cv.waitKey(1)
    if key == ord('c'):
        filename = f"./my_photo_{frame_count}.png"
        cv.imwrite(filename, frame)
        print(f"캡쳐 완료! {filename}")
        frame_count += 1
        break
    elif key == ord('q'):
        break
# 카메라 해제 + 창 닫기
cap.release()
cv.destroyAllWindows()
