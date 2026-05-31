#!/bin/bash
# 라즈베리파이 초기 설정 스크립트
# 실행: bash setup_pi.sh

set -e

echo "패키지 설치 중..."
pip3 install pyserial requests python-dotenv

echo ""
echo "다음 파일을 직접 생성해주세요:"
echo "  nano .env"
echo ""
echo "  내용:"
echo "  KAKAO_CLIENT_ID=your_rest_api_key"
echo "  KAKAO_CLIENT_SECRET=your_client_secret"
echo ""
echo "토큰 발급은 노트북에서 get_token.py 실행 후"
echo "token.json을 이 디렉토리에 복사해주세요."
echo ""

read -p ".env와 token.json 준비됐으면 Enter..."

echo "systemd 서비스 등록 중..."
sudo cp edalf.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable edalf
sudo systemctl start edalf

echo ""
echo "설치 완료!"
echo "상태 확인: sudo systemctl status edalf"
echo "로그 확인: journalctl -u edalf -f"
