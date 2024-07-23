from pin import *
from tire import *
from sensor import *
import time

start_t = time.ticks_ms()
while time.ticks_diff(time.ticks_ms(), start_t) < 2000:
    set_tire(-1, 1)
