# project-edalf

학교 화장실 휴지 잔여량 실시간 모니터링 시스템

## 구성

| 파일 | 설명 |
|------|------|
| `toilet_paper.ino` | Arduino 펌웨어 — HC-SR04 초음파 센서로 휴지 잔여량 측정 |
| `index.html` | 웹 대시보드 — 브라우저에서 직접 열어 아두이노와 연결 |
| `notify.py` | 잔여량 부족 시 카카오톡 알림 전송 (gitignore) |
| `get_token.py` | 카카오 OAuth 토큰 발급 도우미 (gitignore) |

## 하드웨어

| 핀 | 용도 |
|----|------|
| 8 | ECHO (HC-SR04) |
| 9 | TRIG (HC-SR04) |
| 10 | BT RX (SoftwareSerial) |
| 11 | BT TX (SoftwareSerial) |

## 사용법

### 웹 대시보드
1. `index.html`을 Chrome 또는 Edge에서 열기
2. **아두이노 연결** 버튼 클릭 → 포트 선택
3. 실시간으로 칸별 잔여량 확인

### 카카오톡 알림 (선택)
```bash
# 최초 1회 — 카카오 로그인 및 토큰 발급
python get_token.py

# 모니터링 시작
python notify.py
```

> `notify.py` 실행 전 `.env` 파일에 카카오 앱 키를 설정해야 합니다.
> ```
> KAKAO_CLIENT_ID=your_rest_api_key
> KAKAO_CLIENT_SECRET=your_client_secret
> ```

## 잔여량 기준

| 범위 | 상태 |
|------|------|
| 40% 이상 | 충분 |
| 20–39% | 주의 |
| 20% 미만 | 보충 필요 |
