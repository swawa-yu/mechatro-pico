from pin import *
from sensor import *


# 左右に90度回転する関数
def turn_right():
    global direction
    if direction == "W":
        direction = "N"
    elif direction == "N":
        direction = "E"
    elif direction == "E":
        direction = "S"
    elif direction == "S":
        direction = "W"
    pass


def turn_left():
    global direction
    if direction == "W":
        direction = "S"
    elif direction == "S":
        direction = "E"
    elif direction == "E":
        direction = "N"
    elif direction == "N":
        direction = "W"
    pass


# 一定距離進む関数
def move_front(distance):
    """
    distance: [cm]
    """
    # PID制御で真っ直ぐ前に進む
    # d1 > d2 のとき: 左に傾いている　→ 右側のタイヤの出力を小さく(倍率を小さく)
    # d1 < d2 のとき: 右に傾いている　→ 左側のタイヤの出力を小さく(倍率を小さく)
    kp = 1
    ki = 1
    kd = 1
    d1 = get_mtof_distance(i2c1)
    d2 = get_mtof_distance(i2c2)
    pass


# Uターンする関数
# Uターン時に、デフォルトの距離で壁にぶつかる場合はTrue、そうでない場合はFalseを返す。
# distance_to_go: 仮のデフォルト値。実際には、Uターンするために必要な距離を設定する。
def u_turn_right(zigzag_offset=30):
    """
    distance_to_go: [cm]
    """
    global direction
    turn_right()
    move_front(zigzag_offset)
    turn_right()
    return zigzag_offset < 10  # 仮の閾値。


def u_turn_left(distance_to_go=30):
    """
    distance_to_go: [cm]
    """
    global direction
    turn_left()
    move_front(distance_to_go)
    turn_left()
    return distance_to_go < 10  # 仮の閾値。


def set_tire_from_rimocon():
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


def set_tire_left(val):
    if val == -1:
        pin_motor_bin1.value(0)
        pin_motor_bin2.value(1)
    elif val == 0:
        pin_motor_bin1.value(1)
        pin_motor_bin2.value(1)
    elif val == 1:
        pin_motor_bin1.value(1)
        pin_motor_bin2.value(0)


def set_tire_right(val):
    if val == -1:
        pin_motor_ain1.value(1)
        pin_motor_ain2.value(0)
    elif val == 0:
        pin_motor_ain1.value(1)
        pin_motor_ain2.value(1)
    elif val == 1:
        pin_motor_ain1.value(0)
        pin_motor_ain2.value(1)


# 移動方向を設定する関数
def set_direction(dir):
    """
    direction: "forward", "right", "left", "stop" のいずれか
    """
    if dir == "forward":
        set_tire_left(1)
        set_tire_right(1)
    elif dir == "right":
        set_tire_left(1)
        set_tire_right(-1)
    elif dir == "left":
        set_tire_left(-1)
        set_tire_right(1)
    elif dir == "stop":
        set_tire_left(0)
        set_tire_right(0)


def go_to_wall_with_target_collection():
    while not is_front_close_to_wall():
        if is_target_in_roll():  # ターゲットがロールに入った場合
            # 停止し、ターゲットを回収し終えるまで待つ
            set_direction("stop")
            while is_target_in_roll():
                continue
            continue

        # アームの押され方によって進む方向を決定する(壁にぶつかっている状態 or ターゲット(か壁)が左右のにぶつかっている状態 or 何もない状態)
        # match is_right_arm_pressed(), is_left_arm_pressed():
        #     case True, True:
        #         pass  # ルール的にはありえない。もしくは壁にぶつかったことをこれで判定するか。
        #     case True, False:
        #         set_direction("right")
        #     case False, True:
        #         set_direction("left")
        #     case False, False:
        #         # 単に前進...できれば、現在次の壁に到達するまでに保つべき壁との距離を保持しておいて「壁との距離を保ちながら前進」
        #         set_direction("forward")
