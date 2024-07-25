from pin import *
from tire import *
from sensor import *
import time


def level2():
    i = 0
    count = 0

    # while not is_front_close_to_wall():
    d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
    time.sleep_ms(50)
    while d is None:
        pin_debug_y.value(1)
        d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
        time.sleep_ms(50)
    pin_debug_y.value(0)

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
                pin_debug_y.value(1)
                time.sleep(0.5)
                pin_debug_y.value(0)
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
            pin_debug_y.value(1)
            d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
            time.sleep_ms(50)
        pin_debug_y.value(0)

    set_tire(0, 0)
    time.sleep(2)

    # プログラムが終了したらここにくる
    while True:
        pin_debug_y.value(1)
        time.sleep(0.1)
        pin_debug_y.value(0)
        time.sleep(0.1)
