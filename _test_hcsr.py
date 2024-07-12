import machine
import time

# ピンの設定
trigger = machine.Pin(3, machine.Pin.OUT)
echo = machine.Pin(2, machine.Pin.IN)


def get_distance():
    # トリガーを送信
    trigger.low()
    time.sleep_us(2)
    trigger.high()
    time.sleep_us(10)
    trigger.low()

    # エコーの開始時間を取得
    while echo.value() == 0:
        start = time.ticks_us()

    # エコーの終了時間を取得
    while echo.value() == 1:
        end = time.ticks_us()

    # 時間の差分を計算
    duration = time.ticks_diff(end, start)

    # 距離を計算 (音速 = 34300 cm/s)
    distance = (duration * 0.0343) / 2
    return distance


while True:
    dist = get_distance()
    print("Distance: {:.2f} cm".format(dist))
    time.sleep(0.1)


class HCSR04:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger = machine.Pin(trigger_pin, machine.Pin.OUT)
        self.echo = machine.Pin(echo_pin, machine.Pin.IN)

    def get_distance(self):
        # トリガーを送信
        self.trigger.low()
        time.sleep_us(2)
        self.trigger.high()
        time.sleep_us(10)
        self.trigger.low()

        # エコーの開始時間を取得
        while self.echo.value() == 0:
            start = time.ticks_us()

        # エコーの終了時間を取得
        while self.echo.value() == 1:
            end = time.ticks_us()

        # 時間の差分を計算
        duration = time.ticks_diff(end, start)

        # 距離を計算 (音速 = 34300 cm/s)
        distance = (duration * 0.0343) / 2
        return distance
