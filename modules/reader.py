import serial
import threading


class SerialReader(threading.Thread):
    def __init__(self, port, baud_rate, queue):
        super().__init__(daemon=True)
        self.port      = port
        self.baud_rate = baud_rate
        self.queue     = queue

    def run(self):
        print(f"[{self.port}] 연결 중...")
        try:
            ser = serial.Serial(self.port, self.baud_rate, timeout=1)
        except serial.SerialException as e:
            print(f"[{self.port}] 연결 실패: {e}")
            return
        print(f"[{self.port}] 연결 완료.")

        buf = ""
        while True:
            buf += ser.read(64).decode("utf-8", errors="ignore")
            lines = buf.split("\n")
            buf   = lines.pop()
            for line in lines:
                line = line.strip()
                if not line or "," not in line:
                    continue
                stall_id, value = line.split(",", 1)
                self.queue.put((int(stall_id), value.strip()))
