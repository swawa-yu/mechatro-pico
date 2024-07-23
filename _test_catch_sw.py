from pin import *
from tire import *
from sensor import *
import time


pin_debug = Pin(15, Pin.OUT)
while True:
    pin_debug.value(is_catching())
