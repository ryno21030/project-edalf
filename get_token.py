import http.server
import urllib.parse
import webbrowser
import requests
import threading
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID     = os.getenv("KAKAO_CLIENT_ID")
CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET")
REDIRECT_URI  = "http://localhost:8080"
PORT          = 8080

auth_code = None

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<h2>인증 완료! 창을 닫아도 됩니다.</h2>".encode())
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, *args):
        pass

server = http.server.HTTPServer(("", PORT), Handler)
t = threading.Thread(target=server.handle_request)
t.start()

url = (
    f"https://kauth.kakao.com/oauth/authorize"
    f"?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    f"&scope=talk_message&prompt=consent"
)
print("브라우저에서 카카오 로그인 중...")
webbrowser.open(url)

t.join(timeout=120)
if not auth_code:
    print("시간 초과. 다시 실행해주세요.")
    sys.exit(1)

res = requests.post("https://kauth.kakao.com/oauth/token", data={
    "grant_type":    "authorization_code",
    "client_id":     CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri":  REDIRECT_URI,
    "code":          auth_code,
})

if res.status_code != 200:
    print(f"토큰 발급 실패: {res.text}")
    sys.exit(1)

data = res.json()
with open("token.json", "w") as f:
    json.dump({
        "access_token":  data["access_token"],
        "refresh_token": data["refresh_token"],
    }, f)
print("token.json 저장 완료.")
