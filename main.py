from pin import *
from tire import *
from sensor import *
import time

pin_debug = Pin(15, Pin.OUT)
pin_debug.value(0)

# リモコンモード
if pin_rimocon_sw_left1.value() or pin_rimocon_sw_left2.value() or pin_rimocon_sw_right1.value() or pin_rimocon_sw_right2.value():
    pin_debug.value(1)
    # 一旦入力がなくなるまでは何もしない
    while pin_rimocon_sw_left1.value() or pin_rimocon_sw_left2.value() or pin_rimocon_sw_right1.value() or pin_rimocon_sw_right2.value():
        pass

    # リモコンモードに突入したことを知らせる(点滅3回)
    for _ in range(3):
        pin_debug.value(0)
        time.sleep(0.1)
        pin_debug.value(1)
        time.sleep(0.1)

    while True:
        set_tire_from_rimocon()
        pin_debug.value(pin_catch_sw.value())  # リミットスイッチの動作をチェック

# 通常モード
# レベル1だけのクリアを目指す。壁までターゲットを回収しながら前進。
# go_to_wall_with_target_collection() と同じ処理を書いている。テスト用。

i = 0
count = 0

# while not is_front_close_to_wall():
d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
time.sleep_ms(50)
while d is None:
    pin_debug.value(1)
    d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
    time.sleep_ms(50)
pin_debug.value(0)

# while True:
while count < 2:
    print("loop:", i)
    print("catch:", is_catching())

    if is_catching():  # ターゲットがロールに入った場合
        print("target in roll")
        # 停止し(ないで)、しばらく待機(LEDを点滅)
        # TODO: 停止時間の調整
        # set_tire(0, 0)
        for _ in range(3):
            pin_debug.value(1)
            time.sleep(0.5)
            pin_debug.value(0)
            time.sleep(0.5)

        # 回収するまで小刻みに動かす(これがうまくいくかをテスト)
        while is_catching():
            move_forward_and_back_while_target_in_catcher(loop_max=3, speed=0.8, t_forward=0.2, t_back=0.17)
            set_tire(0, 0)
            time.sleep(5)
            # pivot_right_and_left_while_target_in_catcher(t=0.2)

        back_from_right_wall(545, 523)

        count += 1

    # set_tire_from_front_sw()
    set_tire_from_right_wall(545, 523)

    # d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
    # time.sleep_ms(50)
    # while d is None:
    #     pin_debug.value(1)
    #     d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
    #     time.sleep_ms(50)
    # pin_debug.value(0)

    i += 1

while d > 10:
    print("d:", d)
    # set_tire_from_right_wall()
    set_tire(1, 1)

    d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
    time.sleep_ms(50)
    while d is None:
        pin_debug.value(1)
        d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
        time.sleep_ms(50)
    pin_debug.value(0)

set_tire(0, 0)
time.sleep(2)

# 旋回
d1 = get_mtof_distance(i2c1)
while d1 is None:
    d1 = get_mtof_distance(i2c1)
d2 = get_mtof_distance(i2c2)
while d2 is None:
    d2 = get_mtof_distance(i2c2)
while True:
    print("d1:", d1)
    print("d2:", d2)
    if d1 < 150 and d2 < 150 and abs(d1 - d2) < 5:
        break
    set_tire(-0.7, 0.7)

    d1 = get_mtof_distance(i2c1)
    while d1 is None:
        d1 = get_mtof_distance(i2c1)
    d2 = get_mtof_distance(i2c2)
    while d2 is None:
        d2 = get_mtof_distance(i2c2)
    # set_tire(-1, 1)

d1 = get_mtof_distance(i2c1)
while d1 is None:
    d1 = get_mtof_distance(i2c1)
d2 = get_mtof_distance(i2c2)
while d2 is None:
    d2 = get_mtof_distance(i2c2)
while True:
    print("d1:", d1)
    print("d2:", d2)
    if abs(d1 - d2) > 15:
        break
    set_tire(-0.7, 0.7)

    d1 = get_mtof_distance(i2c1)
    while d1 is None:
        d1 = get_mtof_distance(i2c1)
    d2 = get_mtof_distance(i2c2)
    while d2 is None:
        d2 = get_mtof_distance(i2c2)

d1 = get_mtof_distance(i2c1)
while d1 is None:
    d1 = get_mtof_distance(i2c1)
d2 = get_mtof_distance(i2c2)
while d2 is None:
    d2 = get_mtof_distance(i2c2)
while True:
    print("d1:", d1)
    print("d2:", d2)
    if abs(d1 - d2) < 10:
        break
    set_tire(-0.7, 0.7)

    d1 = get_mtof_distance(i2c1)
    while d1 is None:
        d1 = get_mtof_distance(i2c1)
    d2 = get_mtof_distance(i2c2)
    while d2 is None:
        d2 = get_mtof_distance(i2c2)

set_tire(0, 0)
time.sleep(2)

i = 0
count = 0

# while not is_front_close_to_wall():
d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
time.sleep_ms(50)
while d is None:
    pin_debug.value(1)
    d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
    time.sleep_ms(50)
pin_debug.value(0)

# while True:
while count < 3:
    print("loop:", i)
    print("catch:", is_catching())

    if is_catching():  # ターゲットがロールに入った場合
        print("target in roll")
        # 停止し(ないで)、しばらく待機(LEDを点滅)
        # TODO: 停止時間の調整
        # set_tire(0, 0)
        for _ in range(3):
            pin_debug.value(1)
            time.sleep(0.5)
            pin_debug.value(0)
            time.sleep(0.5)

        # 回収するまで小刻みに動かす(これがうまくいくかをテスト)
        while is_catching():
            move_forward_and_back_while_target_in_catcher(loop_max=3, speed=0.8, t_forward=0.2, t_back=0.17)
            set_tire(0, 0)
            time.sleep(5)
            # pivot_right_and_left_while_target_in_catcher(t=0.2)

        back_from_right_wall(294, 288)

        count += 1

    # set_tire_from_front_sw()
    set_tire_from_right_wall(294, 288)

    # d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
    # time.sleep_ms(50)
    # while d is None:
    #     pin_debug.value(1)
    #     d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
    #     time.sleep_ms(50)
    # pin_debug.value(0)

    i += 1

while d > 10:
    print("d:", d)
    # set_tire_from_right_wall()
    set_tire(1, 1)

    d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
    time.sleep_ms(50)
    while d is None:
        pin_debug.value(1)
        d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
        time.sleep_ms(50)
    pin_debug.value(0)

set_tire(0, 0)
time.sleep(2)

# プログラムが終了したらここにくる
while True:
    pin_debug.value(1)
    time.sleep(0.1)
    pin_debug.value(0)
    time.sleep(0.1)
