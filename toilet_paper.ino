#include <SoftwareSerial.h>

SoftwareSerial bt(10, 11); // RX=10, TX=11

const int TRIG = 9;
const int ECHO = 8;

// 센서에서 롤 중심까지 거리(cm) — 홀더 크기에 따라 조정
const float SENSOR_TO_CENTER = 8.0;

// 새 롤 반지름 / 빈 코어 반지름 (cm)
const float FULL_RADIUS  = 5.0;
const float EMPTY_RADIUS = 2.0;

float measureDistance() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  long duration = pulseIn(ECHO, HIGH, 30000); // 30ms timeout
  if (duration == 0) return -1; // 측정 실패
  return duration * 0.034 / 2.0;
}

int calcRemaining(float distance) {
  float radius = SENSOR_TO_CENTER - distance;
  radius = constrain(radius, EMPTY_RADIUS, FULL_RADIUS);
  return (int)((radius - EMPTY_RADIUS) / (FULL_RADIUS - EMPTY_RADIUS) * 100.0);
}

void setup() {
  Serial.begin(9600);
  bt.begin(9600);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
}

void loop() {
  float distance = measureDistance();

  if (distance < 0) {
    bt.println("ERR");
    Serial.println("측정 실패");
  } else {
    int remaining = calcRemaining(distance);
    bt.println(remaining);         // 앱으로 전송 (예: "73")
    Serial.print("잔량: ");
    Serial.print(remaining);
    Serial.println("%");
  }

  delay(3000); // 3초마다 전송
}
