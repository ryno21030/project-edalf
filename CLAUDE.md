# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

학교 화장실 휴지 잔여량 실시간 모니터링 시스템. 두 개의 레이어로 구성됩니다:

1. **Arduino firmware** (`toilet_paper.ino`) — HC-SR04 초음파 센서로 휴지 롤 반지름을 측정하고, SoftwareSerial(Bluetooth)로 잔여량(%)을 3초마다 전송
2. **Web dashboard** (`index.html`) — 브라우저에서 바로 열 수 있는 단일 HTML 파일. 각 칸별 잔여량을 게이지 바 카드로 표시

## Architecture

### Arduino → Web 데이터 흐름

```text
HC-SR04 센서 → Arduino(핀 8/9) → calcRemaining() → Bluetooth(핀 10/11) → 앱/웹
```

- 센서에서 롤 중심까지의 거리를 측정해 반지름으로 역산
- `SENSOR_TO_CENTER`, `FULL_RADIUS`, `EMPTY_RADIUS` 상수로 홀더 크기 조정
- Bluetooth로 정수 문자열(`"73"`) 또는 `"ERR"` 전송

### Web Dashboard

- `stalls` 배열이 유일한 데이터 소스 — 아두이노 연동 시 이 배열을 실시간 업데이트로 교체
- 잔여량 임계값: ≥40% 충분(초록), 20–39% 주의(주황), <20% 보충 필요(빨강)
- `simulateUpdate()` 버튼으로 랜덤 변동 테스트 가능

## Running

```bash
# 웹 대시보드 — 브라우저에서 직접 열기
start index.html

# Arduino 펌웨어 — VSCode Arduino 확장 또는 Arduino IDE에서 업로드
# 보드: Arduino Uno / 포트: COMx
```

## Hardware Pin Map

| 핀 | 용도                   |
|----|------------------------|
| 8  | ECHO (HC-SR04)         |
| 9  | TRIG (HC-SR04)         |
| 10 | BT RX (SoftwareSerial) |
| 11 | BT TX (SoftwareSerial) |
