from pin import *
from machine import I2C
from machine import Pin
import time

# MTOF171000C0のアドレス(ModuleID)です。
MTOF_ADDRESS = 0x52

print("mtof_test start.")

# I2Cのピンの設定です
i2c1 = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000)
i2c2 = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
# i2c1 = I2C(1, scl=pin_mtof1_scl, sda=pin_mtof1_sda, freq=100000)
# i2c2 = I2C(0, scl=pin_mtof2_scl, sda=pin_mtof2_sda, freq=100000)


# GPIOのピンの設定です
# センサの「モジュール選択ピン(センサのRxD)」操作に使います
# pin4 = Pin(4, Pin.OUT)

# Picoの処理待ちです。
time.sleep_ms(1000)

# センサにデータ送信を伝えるため、選択ピンをLowにします
# pin4.value(0)

# センサの処理待ちで、5msec待ちます。
time.sleep_ms(5)


def get_distance(num):
    i2c = i2c1 if num == 1 else i2c2
    # データ取得要求を送信します(0xD3)
    cmd = bytearray(1)
    cmd[0] = 0xD3
    i2c.writeto(MTOF_ADDRESS, cmd)

    # データを受信します
    data = i2c.readfrom(MTOF_ADDRESS, 2)

    # 受信データを距離に変換します
    distance = (data[0] << 8) | data[1]
    return distance


while True:
    # # データ取得要求を送信します(0xD3)
    # cmd = bytearray(1)
    # cmd[0] = 0xD3
    # i2c1.writeto(MTOF_ADDRESS, cmd)

    # # データを受信します
    # data = i2c1.readfrom(MTOF_ADDRESS, 2)

    # # 受信データを距離に変換します
    # distance = (data[0] << 8) | data[1]
    # print(f"1: {distance} mm")

    # # データ取得要求を送信します(0xD3)
    # cmd = bytearray(1)
    # cmd[0] = 0xD3
    # i2c2.writeto(MTOF_ADDRESS, cmd)

    # # データを受信します
    # data = i2c2.readfrom(MTOF_ADDRESS, 2)

    # # 受信データを距離に変換します
    # distance = (data[0] << 8) | data[1]
    # print(f"2: {distance} mm")

    print(f"1: {get_distance(1)} mm")
    print(f"2: {get_distance(2)} mm")
    time.sleep(1)


# 初期値を設定します
prev_distance = None
threshold = 100  # 突然変化とみなす距離の変化量（単位：mm）

for i in range(100000):

    # データ取得要求を送信します(0xD3)
    cmd = bytearray(1)
    cmd[0] = 0xD3
    i2c1.writeto(MTOF_ADDRESS, cmd)

    # データを受信します
    data = i2c1.readfrom(MTOF_ADDRESS, 2)

    # 受信データを距離に変換します
    distance = (data[0] << 8) | data[1]

    # 距離が突然短くなったら、その距離を出力
    if prev_distance is not None and distance - prev_distance < -threshold:
        print(f"Distance changed suddenly: {distance} [mm]")

    # 現在の距離を前回の距離として保存します
    prev_distance = distance

    # ループ間隔の調整です（0.01ms = 10µs）
    time.sleep_us(10)

# デバイスに通信終了を知らせるために、
# モジュール選択ピンをHighにします
# pin4.value(1)

print("done")
