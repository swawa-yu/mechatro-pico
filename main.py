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

# while not is_front_close_to_wall():
d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
time.sleep_ms(50)
while d is None:
    pin_debug.value(1)
    d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
    time.sleep_ms(50)
pin_debug.value(0)

while d > 30:
    print("loop:", i)
    print("d:", d)
    print("catch:", is_catching())

    if is_catching():  # ターゲットがロールに入った場合
        print("target in roll")
        # 停止し、しばらく待機(LEDを点滅)
        # TODO: 停止時間の調整
        set_tire(0, 0)
        for _ in range(3):
            pin_debug.value(1)
            time.sleep(0.5)
            pin_debug.value(0)
            time.sleep(0.5)

        # 回収するまで小刻みに動かす(これがうまくいくかをテスト)
        while is_catching():
            move_forward_and_back_while_target_in_catcher()
            pivot_right_and_left_while_target_in_catcher()

    set_tire_from_front_sw()

    d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
    time.sleep_ms(50)
    while d is None:
        pin_debug.value(1)
        d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
        time.sleep_ms(50)
    pin_debug.value(0)

    i += 1
