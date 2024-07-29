from pin import *
from tire import *
from sensor import *
import time


def level1_to_level2():
    # 旋回
    # 西の壁に対して平行になるまで反時計回り(90°回転)
    d1, d2 = get_mtof_distance(i2c1), get_mtof_distance(i2c2)
    while not (d1 < 150 and d2 < 150 and abs(d1 - d2) < 5):
        set_tire(-0.7, 0.7)
        d1, d2 = get_mtof_distance(i2c1), get_mtof_distance(i2c2)

    # 切れ目を停止で確認
    set_tire(0, 0)
    time.sleep(2)

    move_back(10)

    # 一旦壁に対して平行でなくなるまで反時計回り
    d1, d2 = get_mtof_distance(i2c1), get_mtof_distance(i2c2)
    while not (abs(d1 - d2) > 15):
        set_tire(-0.7, 0.7)
        d1, d2 = get_mtof_distance(i2c1), get_mtof_distance(i2c2)

    # (南の)壁に対して平行になるまで反時計回り(90°回転)
    d1, d2 = get_mtof_distance(i2c1), get_mtof_distance(i2c2)
    while not (abs(d1 - d2) < 10):
        set_tire(-0.7, 0.7)
        d1, d2 = get_mtof_distance(i2c1), get_mtof_distance(i2c2)

    # 停止
    set_tire(0, 0)
    time.sleep(2)
