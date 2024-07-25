from pin import *
from tire import *
from sensor import *
import time

from main_lv1 import level1
from main_lv2 import level2


pin_debug_y.value(0)


# リモコンモード
if pin_rimocon_sw_left1.value() or pin_rimocon_sw_left2.value() or pin_rimocon_sw_right1.value() or pin_rimocon_sw_right2.value():
    pin_debug_y.value(1)
    # 一旦入力がなくなるまでは何もしない
    while pin_rimocon_sw_left1.value() or pin_rimocon_sw_left2.value() or pin_rimocon_sw_right1.value() or pin_rimocon_sw_right2.value():
        pass

    # リモコンモードに突入したことを知らせる(点滅3回)
    for _ in range(3):
        pin_debug_y.value(0)
        time.sleep(0.1)
        pin_debug_y.value(1)
        time.sleep(0.1)

    while True:
        set_tire_from_rimocon()
        pin_debug_y.value(pin_catch_sw.value())  # リミットスイッチの動作をチェック

# 通常モード
# レベル1だけのクリアを目指す。壁までターゲットを回収しながら前進。
level1()

# 旋回
# 西の壁に対して平行になるまで反時計回り(90°回転)
d1, d2 = get_mtof_distance(i2c1), get_mtof_distance(i2c2)
while not (d1 < 150 and d2 < 150 and abs(d1 - d2) < 5):
    set_tire(-0.7, 0.7)
    d1, d2 = get_mtof_distance(i2c1), get_mtof_distance(i2c2)

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

level2()
