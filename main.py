from pin import *
from tire import *
from sensor import *
import time

from main_lv1 import level1
from main_lv1tolv2 import level1_to_level2
from main_lv2 import level2
from main_lv2tolv3 import level2_to_level3
from main_lv3 import level3


pin_debug_y.value(0)
pin_debug_g.value(0)
pin_debug_g_gnd.value(0)
pin_debug_r.value(0)
pin_debug_r_gnd.value(0)

# リモコンモード
if pin_rimocon_sw_left1.value() or pin_rimocon_sw_left2.value() or pin_rimocon_sw_right1.value() or pin_rimocon_sw_right2.value():
    print("rimocon mode")
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

print("normal mode")

# デバッグ用ピンの初期化
pin_debug_y.value(0)
pin_debug_g.value(0)
pin_debug_g_gnd.value(0)
pin_debug_r.value(0)
pin_debug_r_gnd.value(0)


# 通常モード
level1()
level1_to_level2()
level2()
level2_to_level3()
level3()


# プログラムが終了したらここにくる
while True:
    pin_debug_y.value(1)
    time.sleep(0.1)
    pin_debug_y.value(0)
    time.sleep(0.1)
