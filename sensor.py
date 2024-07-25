from pin import *
from machine import I2C
import time

print("init sensor settings (in sensor.py)")
MTOF_ADDRESS = 0x52

# I2Cのピンの設定です
i2c1 = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000)
i2c2 = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)

print("  (waiting 1sec for processing.)")
time.sleep_ms(1000)


import time


def get_hcsr_distance(trig, echo, timeout=10000):
    """
    return: cm
    """
    # トリガーを送信
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()

    # タイムアウト用の開始時間
    start_time = time.ticks_us()
    start = start_time

    # エコーの開始時間を取得
    while echo.value() == 0:
        if time.ticks_diff(time.ticks_us(), start_time) > timeout:
            return None
        start = time.ticks_us()

    # エコーの終了時間を取得
    while echo.value() == 1:
        if time.ticks_diff(time.ticks_us(), start) > timeout:
            return None
        end = time.ticks_us()

    # 時間の差分を計算
    duration = time.ticks_diff(end, start)

    # 距離を計算 (音速 = 34300 cm/s)
    distance = (duration * 0.0343) / 2
    return distance


def try_to_get_mtof_distance(i2c):
    """
    return: mm
    """
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


def get_mtof_distance(i2c):
    """
    return: mm
    """
    d = try_to_get_mtof_distance(i2c)
    while d is None:
        d = try_to_get_mtof_distance(i2c)
    print("d1:" if i2c == i2c1 else "d2:", d)
    return d


# 各種センサーにより状態を得る関数
def is_front_close_to_wall():
    pass


def is_right_arm_pressed():
    return pin_front_sw_r.value()


def is_left_arm_pressed():
    return pin_front_sw_l.value()


def is_close_to_right_wall():
    pass


def is_close_to_left_wall():
    pass


def is_catching():
    return not pin_catch_sw.value()


def is_target_detected():
    pass


def distance_to_front():
    return get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)


def is_direction_north():
    return True  # 実際にはセンサーの値を元に判断する。


print("finish init sensor settings (in sensor.py)")
