# GPIO 14, 15のHIGH/LOWを切り替えてモーターを動かすテスト
# 1秒間隔で回転方向を切り替える

import machine
import time

in1 = machine.Pin(14, machine.Pin.OUT)
in2 = machine.Pin(15, machine.Pin.OUT)

while True:
    # in1.value(0)
    # in2.value(0)
    # time.sleep(1)

    in1.value(0)
    in2.value(1)
    time.sleep(1)

    in1.value(1)
    in2.value(1)
    time.sleep(0.1)

    in1.value(1)
    in2.value(0)
    time.sleep(1)

    in1.value(1)
    in2.value(1)
    time.sleep(0.1)
