# project-edalf

학교 화장실 휴지 잔여량 실시간 모니터링 시스템

## 구성 파일

| 파일 | 설명 |
|------|------|
| `toilet_paper.ino` | Arduino 펌웨어 — HC-SR04 초음파 센서로 휴지 잔여량 측정 |
| `notify.py` | 잔여량 부족 시 카카오톡 알림 전송 |
| `get_token.py` | 카카오 OAuth 토큰 발급 도우미 |
| `edalf.service` | 라즈베리파이 systemd 자동 실행 서비스 |
| `setup_pi.sh` | 라즈베리파이 초기 설정 스크립트 |

## 준비물

### 하드웨어

| 부품 | 설명 |
|------|------|
| Arduino Uno (또는 Nano) | 메인 컨트롤러 |
| HC-SR04 | 초음파 거리 센서 |
| HC-06 (또는 HC-05) | 블루투스 모듈 |
| 라즈베리파이 (선택) | 상시 실행 서버 |

### 아두이노 핀 연결

| 핀 | 용도 |
|----|------|
| 8 | ECHO (HC-SR04) |
| 9 | TRIG (HC-SR04) |
| 10 | BT RX (SoftwareSerial) |
| 11 | BT TX (SoftwareSerial) |

### Python 패키지

```bash
pip install -r requirements.txt
```

| 패키지 | 용도 |
|--------|------|
| `pyserial` | 시리얼/블루투스 통신 |
| `requests` | 카카오 API 호출 |
| `python-dotenv` | `.env` 파일에서 환경변수 로드 |

### 카카오 설정

- [카카오 개발자 콘솔](https://developers.kakao.com)에서 앱 생성
- 카카오 로그인 활성화 및 `talk_message` 동의항목 설정
- Redirect URI: `http://localhost:8080` 등록

`.env` 파일 생성:

```env
KAKAO_CLIENT_ID=your_rest_api_key
KAKAO_CLIENT_SECRET=your_client_secret
```

## 사용법

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 최초 1회 — 카카오 로그인 및 토큰 발급
python get_token.py

# 3. 모니터링 시작
python notify.py
```

## 잔여량 기준

| 범위 | 상태 |
|------|------|
| 40% 이상 | 충분 |
| 20–39% | 주의 |
| 20% 미만 | 보충 필요 |
