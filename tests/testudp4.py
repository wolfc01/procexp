import socket
import sys
import threading
import time

portFrom = int(sys.argv[1])
toIP   = sys.argv[2]
portTo = int(sys.argv[3])

bytespersec   = int(sys.argv[4])
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", portFrom))

def send():
    while True:
        s.sendto(b"a"*int(bytespersec/10+0.5), (toIP, portTo))
        time.sleep(0.1)

t = threading.Thread(daemon=True, target=send)
t.start()

while True:
    data = s.recvfrom(1024)

