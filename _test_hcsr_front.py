from pin import *
from tire import *
from sensor import *
import time

while True:
    d = get_hcsr_distance(pin_front_hcsr_trig, pin_front_hcsr_echo)
    time.sleep_ms(50)
    print("d:", d)
