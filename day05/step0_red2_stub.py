import serial
import time

def send_command(ser,command):
    return False

ser = None

result = send_command(ser,'O')
if result:
    print("✅ PASS: 아두이노 명령 전송 성공!")
else:
    print("❌ FAIL: send_command() 함수가 아직 구현되지 않았습니다.")

result = send_command(ser,'C')
if result:
    print("✅ PASS: 문 닫기 명령 전송 성공!")
else:
    print("❌ FAIL: send_command() 함수가 아직 구현되지 않았습니다.")
