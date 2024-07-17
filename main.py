from pin import *
from tire import *
from sensor import *
import time


# start = time.ticks_ms()
# t = time.ticks_ms()
# set_tire_left(1)
# set_tire_right(1)
# while time.ticks_diff(t, start) < 5000:
#     t = time.ticks_ms()
#     pass

pin_debug = Pin(15, Pin.OUT)
pin_debug.value(1)

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
    pin_debug.value(0)
    move_front(100)
    set_tire_left(0)
    set_tire_right(0)


# p = 0

# for p in range(11):
#     print(p)
#     set_tire_left(p / 10)
#     set_tire_right(p / 10)
# time.sleep_ms(1000)


# set_tire_left(1)
# set_tire_right(0.97)
# time.sleep_ms(5000)
# set_tire_left(0)
# set_tire_right(0)


# d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
# while d is None:
#     time.sleep_ms(50)
#     d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
# print(d)

# set_tire_left(1)
# set_tire_right(1)

# # while True:
# while d > 50:
#     time.sleep_ms(50)
#     d_ = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
#     print(d_)
#     if d_ is None:
#         print("d is None")
#         break

#     if abs(d - d_) > 5:
#         print("invalid d (continue)")
#         continue
#     else:
#         d = d_


# set_tire_left(0)
# set_tire_right(0)
