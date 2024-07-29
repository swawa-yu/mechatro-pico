from pin import *
from tire import *
from sensor import *
import time


pin_debug_y = Pin(15, Pin.OUT)
while True:
    pin_debug_y.value(is_catching())
