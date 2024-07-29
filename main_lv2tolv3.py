from pin import *
from tire import *
from sensor import *
import time


def level2_to_level3():
    # 旋回
    pin_debug_g.value(1)
    # 一旦西の壁に対して平行でなくなるまで反時計回り(90°回転)
    d1, d2 = get_mtof_distance(i2c1), get_mtof_distance(i2c2)
    while d1 - d2 < 50:
        set_tire(-0.7, 0)
        d1, d2 = get_mtof_distance(i2c1), get_mtof_distance(i2c2)

    # 西の壁に対して平行になるまで反時計回り(90°回転)
    d1, d2 = get_mtof_distance(i2c1), get_mtof_distance(i2c2)
    while abs(d1 - d2) > 10:
        set_tire(-0.7, 0)
        d1, d2 = get_mtof_distance(i2c1), get_mtof_distance(i2c2)
    pin_debug_g.value(0)

    # 切れ目を停止で確認
    set_tire(0, 0)
    time.sleep(2)
    pin_debug_g.value(1)

    # 北側の壁に対して15cmまで前進
    sd = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
    while sd - get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo) < 15:
        set_tire_from_right_wall()
        time.sleep_ms(50)

    pin_debug_g.value(0)

    # 切れ目を停止で確認
    set_tire(0, 0)
    time.sleep(2)
    pin_debug_g.value(1)

    # 一旦壁に対して平行でなくなるまで反時計回り
    d1, d2 = get_mtof_distance(i2c1), get_mtof_distance(i2c2)
    while d1 - d2 < 50:
        set_tire(0, 0.7)
        d1, d2 = get_mtof_distance(i2c1), get_mtof_distance(i2c2)

    # (北の)壁に対して平行になるまで反時計回り(90°回転)
    d1, d2 = get_mtof_distance(i2c1), get_mtof_distance(i2c2)
    while abs(d1 - d2) > 10:
        set_tire(0, 0.7)
        d1, d2 = get_mtof_distance(i2c1), get_mtof_distance(i2c2)

    pin_debug_g.value(0)
    # 停止
    set_tire(0, 0)
    time.sleep(2)
