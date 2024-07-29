from pin import *
from tire import *
from sensor import *
import time


pin_debug_y = Pin(15, Pin.OUT)
pin_debug_y.value(1)

# リモコンモード
if pin_rimocon_sw_left1.value() or pin_rimocon_sw_left2.value() or pin_rimocon_sw_right1.value() or pin_rimocon_sw_right2.value():
    while True:
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

# 通常モード
else:
    pin_debug_y.value(0)

    # キャッチするまで前進
    while not pin_catch_sw.value():
        set_tire_left(1)
        set_tire_right(1)

    # 停止
    set_tire_left(0)
    set_tire_right(0)
