import json
import threading
import time
import requests
from . import token as token_mod

_lock = threading.Lock()


class Notifier:
    def __init__(self, warn_level=20, cooldown=600):
        self.warn_level   = warn_level
        self.cooldown     = cooldown
        self._tokens      = token_mod.load()
        self._last        = {}

    def handle(self, stall_id, level):
        if level >= self.warn_level:
            return
        now = time.time()
        if now - self._last.get(stall_id, 0) < self.cooldown:
            return
        if self._send(stall_id, level):
            print(f"[칸 {stall_id}] 카카오톡 알림 전송 완료")
            self._last[stall_id] = now
        else:
            print(f"[칸 {stall_id}] 알림 전송 실패")

    def _send(self, stall_id, level):
        with _lock:
            template = {
                "object_type": "text",
                "text": f"⚠️ 화장실 {stall_id}번 칸 휴지 부족\n현재 잔량: {level}%\n보충이 필요합니다.",
                "link": {"web_url": "", "mobile_web_url": ""},
            }
            ok, self._tokens = self._post(template)
            return ok

    def _post(self, template):
        url     = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        headers = {
            "Authorization": f"Bearer {self._tokens['access_token']}",
            "Content-Type":  "application/x-www-form-urlencoded",
        }
        data = {"template_object": json.dumps(template)}
        res  = requests.post(url, headers=headers, data=data)

        if res.status_code == 401:
            self._tokens = token_mod.refresh(self._tokens)
            headers["Authorization"] = f"Bearer {self._tokens['access_token']}"
            res = requests.post(url, headers=headers, data=data)

        if res.status_code != 200:
            print(f"[카카오 API 오류] {res.status_code}: {res.text}")
            return False, self._tokens
        return True, self._tokens
