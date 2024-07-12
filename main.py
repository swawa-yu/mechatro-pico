from pin import *
from tire import *
from sensor import *
import time


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
