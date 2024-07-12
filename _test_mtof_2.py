from pin import *
from machine import I2C, Pin
import time

# MTOF171000C0のアドレス(ModuleID)です。
MTOF_ADDRESS = 0x52

print("mtof_test start.")

# I2Cのピンの設定です
i2c1 = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000)
i2c2 = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)

# Picoの処理待ちです。
time.sleep_ms(1000)

# センサの処理待ちで、5msec待ちます。
time.sleep_ms(5)


def get_distance(i2c):
    try:
        cmd = bytearray(1)
        cmd[0] = 0xD3
        i2c.writeto(MTOF_ADDRESS, cmd)
        data = i2c.readfrom(MTOF_ADDRESS, 2)
        distance = (data[0] << 8) | data[1]
        return distance
    except OSError as e:
        print(f"I2C error: {e}")
        return None


while True:
    distance1 = get_distance(i2c1)
    distance2 = get_distance(i2c2)
    if distance1 is not None and distance2 is not None:
        print(f"Distance: {distance1} {distance2}")
    # if distance2 is not None:
    #     print(f"Distance2: {distance2}")
    time.sleep(0.1)
