import json
import threading
import requests
import os

TOKEN_FILE = "token.json"
_lock = threading.Lock()


def load():
    try:
        with open(TOKEN_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit("token.json 없음. get_token.py 를 먼저 실행하세요.")


def refresh(tokens):
    with _lock:
        res = requests.post("https://kauth.kakao.com/oauth/token", data={
            "grant_type":    "refresh_token",
            "client_id":     os.getenv("KAKAO_CLIENT_ID"),
            "client_secret": os.getenv("KAKAO_CLIENT_SECRET"),
            "refresh_token": tokens["refresh_token"],
        })
        if res.status_code != 200:
            raise SystemExit(f"토큰 갱신 실패: {res.text}")
        data = res.json()
        updated = {
            "access_token":  data["access_token"],
            "refresh_token": data.get("refresh_token", tokens["refresh_token"]),
        }
        with open(TOKEN_FILE, "w") as f:
            json.dump(updated, f)
        print("[토큰 갱신 완료]")
        return updated
