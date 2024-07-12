from pin import *
from tire import *
from sensor import *
import time

pin_rimocon_sw_left1 = Pin(16, Pin.IN, Pin.PULL_DOWN)
pin_rimocon_sw_left2 = Pin(17, Pin.IN, Pin.PULL_DOWN)
pin_rimocon_sw_right1 = Pin(18, Pin.IN, Pin.PULL_DOWN)
pin_rimocon_sw_right2 = Pin(19, Pin.IN, Pin.PULL_DOWN)


def set_tire_from_rimocon():
    l1 = pin_rimocon_sw_left1.value()
    l2 = pin_rimocon_sw_left2.value()
    r1 = pin_rimocon_sw_right1.value()
    r2 = pin_rimocon_sw_right2.value()

    if l1 == 1 and l2 == 0:
        set_tire_left(1)
    elif l1 == 0 and l2 == 1:
        set_tire_left(-1)
    else:
        set_tire_left(0)

    if r1 == 1 and r2 == 0:
        set_tire_right(1)
    elif r1 == 0 and r2 == 1:
        set_tire_right(-1)
    else:
        set_tire_right(0)


start = time.ticks_us()
while True:
    t = time.ticks_diff(time.ticks_us, start)
    print(f"----time: {t}us")

    # リモコンの入力に応じてタイヤの動作を設定
    set_tire_from_rimocon()

    # センサーの動作を確認(測定値を出力)
    d_mtof_front = get_mtof_distance(i2c1)
    d_mtof_back = get_mtof_distance(i2c2)
    d_hcsr_front = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
    d_hcsr_right = get_hcsr_distance(pin_right_hcsr_trig, pin_right_hcsr_echo)
    # print(f"MTOF front: {d_mtof_front}")
    # print(f"MTOF back : {d_mtof_back}")
    # print(f"HCSR front: {d_hcsr_front}")
    # print(f"HCSR right: {d_hcsr_right}")

    # time.sleep(1)
