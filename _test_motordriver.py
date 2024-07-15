from pin import *
from tire import *
import time

pin_rimocon_sw_left1 = Pin(16, Pin.IN, Pin.PULL_DOWN)
pin_rimocon_sw_left2 = Pin(17, Pin.IN, Pin.PULL_DOWN)
pin_rimocon_sw_right1 = Pin(18, Pin.IN, Pin.PULL_DOWN)
pin_rimocon_sw_right2 = Pin(19, Pin.IN, Pin.PULL_DOWN)

pin_front_sw_r = Pin(1, Pin.OUT)
pin_front_sw_r.value(1)

while True:
    set_tire_left(1)
    set_tire_right(1)
    time.sleep(1)

    # set_tire_left(0)
    # set_tire_right(0)
    # time.sleep(1)

    set_tire_left(-1)
    set_tire_right(-1)
    time.sleep(1)

    # set_tire_left(0)
    # set_tire_right(0)
    # time.sleep(1)
