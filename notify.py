import os
import queue
from dotenv import load_dotenv
from modules.reader   import SerialReader
from modules.notifier import Notifier

load_dotenv()

PORTS      = [p.strip() for p in os.getenv("SERIAL_PORTS", "/dev/ttyUSB0").split(",")]
BAUD_RATE  = int(os.getenv("BAUD_RATE", 9600))
WARN_LEVEL = int(os.getenv("WARN_LEVEL", 20))
COOLDOWN   = int(os.getenv("COOLDOWN",   600))

data_queue = queue.Queue()
notifier   = Notifier(warn_level=WARN_LEVEL, cooldown=COOLDOWN)

for port in PORTS:
    SerialReader(port, BAUD_RATE, data_queue).start()

print(f"모니터링 시작 ({len(PORTS)}개 포트)")

while True:
    stall_id, value = data_queue.get()
    if value == "ERR":
        print(f"[칸 {stall_id}] 측정 오류")
        continue
    level = int(value)
    print(f"[칸 {stall_id}] 잔량 {level}%")
    notifier.handle(stall_id, level)
