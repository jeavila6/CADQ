import threading
from collections import deque


class SerialReader(threading.Thread):

    def __init__(self, port):
        super().__init__(daemon=True)
        self.port = port
        self.active = True

        # queue contains only latest reading at any time
        initial_queue = ['1']
        self.stream = deque(initial_queue, maxlen=1)

    def run(self):
        """Read from serial port into queue until stopped."""
        while self.active:
            data = self.port.readline().decode('ascii').strip()
            if data:
                self.stream.append(data)

    def stop(self):
        """Stop reading from serial port."""
        self.active = False
