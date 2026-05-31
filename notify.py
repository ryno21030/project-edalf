import serial
import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID     = os.getenv("KAKAO_CLIENT_ID")
CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET")
TOKEN_FILE    = "token.json"
COM_PORT      = "/dev/ttyUSB0"
BAUD_RATE     = 9600
WARN_LEVEL    = 20
COOLDOWN      = 600

def load_tokens():
    try:
        with open(TOKEN_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit("token.json 없음. get_token.py 를 먼저 실행하세요.")

def refresh_access_token(refresh_token):
    res = requests.post("https://kauth.kakao.com/oauth/token", data={
        "grant_type":    "refresh_token",
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token,
    })
    if res.status_code != 200:
        raise SystemExit(f"토큰 갱신 실패: {res.text}")
    data = res.json()
    tokens = {
        "access_token":  data["access_token"],
        "refresh_token": data.get("refresh_token", refresh_token),
    }
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f)
    print("[토큰 갱신 완료]")
    return tokens

def send_kakao(stall_id, level, tokens):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    template = {
        "object_type": "text",
        "text": f"⚠️ 화장실 {stall_id}번 칸 휴지 부족\n현재 잔량: {level}%\n보충이 필요합니다.",
        "link": {"web_url": "", "mobile_web_url": ""},
    }
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    res = requests.post(url, headers=headers, data={"template_object": json.dumps(template)})

    if res.status_code == 401:
        tokens = refresh_access_token(tokens["refresh_token"])
        headers["Authorization"] = f"Bearer {tokens['access_token']}"
        res = requests.post(url, headers=headers, data={"template_object": json.dumps(template)})

    if res.status_code != 200:
        print(f"[카카오 API 오류] {res.status_code}: {res.text}")
        return False, tokens
    return True, tokens

tokens = load_tokens()
last_notified = {}

print(f"{COM_PORT} 연결 중...")
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
print("연결 완료. 모니터링 시작.")

buf = ""
while True:
    buf += ser.read(64).decode("utf-8", errors="ignore")
    lines = buf.split("\n")
    buf = lines.pop()

    for line in lines:
        line = line.strip()
        if not line or "," not in line:
            continue

        stall_id, value = line.split(",", 1)
        stall_id = int(stall_id)

        if value == "ERR":
            print(f"[칸 {stall_id}] 측정 오류")
            continue

        level = int(value)
        print(f"[칸 {stall_id}] 잔량 {level}%")

        now  = time.time()
        last = last_notified.get(stall_id, 0)

        if level < WARN_LEVEL and (now - last) > COOLDOWN:
            ok, tokens = send_kakao(stall_id, level, tokens)
            if ok:
                print(f"[칸 {stall_id}] 카카오톡 알림 전송 완료")
                last_notified[stall_id] = now
            else:
                print(f"[칸 {stall_id}] 알림 전송 실패")
