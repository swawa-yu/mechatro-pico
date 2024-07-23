from pin import *
from tire import *
from sensor import *
import time

l_d1 = []
l_d2 = []
while True:
    l_d1.append(get_mtof_distance(i2c1))
    l_d2.append(get_mtof_distance(i2c2))

    if len(l_d1) > 1000:
        l_d1.pop(0)
        l_d2.pop(0)

    print("d1:", sum(l_d1) / len(l_d1))
    print("d2:", sum(l_d2) / len(l_d2))
    # time.sleep(0.5)
