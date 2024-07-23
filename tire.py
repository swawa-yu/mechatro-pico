from pin import *
from sensor import *
import math

print("init tire settings (in tire.py)")

direction = 2


# 左右に90度回転する関数
def turn_right():
    global direction
    direction = (direction - 1) % 4
    pass


def turn_left():
    global direction
    direction = (direction + 1) % 4
    pass


d12 = None
dd12 = None
sd12 = 0


# TODO: 壁から遠いときの誤差の調整
def rotback_from_right_wall():
    while True:
        d1 = get_mtof_distance(i2c1)
        d2 = get_mtof_distance(i2c2)
        if d1 is None or d2 is None:
            continue
        d12 = d1 - d2

        # 一定の範囲内に収まったら良しとする
        if abs(d12) < 10:
            return

        # 壁でなくターゲットとの距離を測ってしまった場合は下がる
        if abs(d12) > 100:
            set_tire(-0.5, -0.5)
            continue

        if d12 > 0:
            set_tire(0, -0.5)
        else:
            set_tire(-0.5, 0)


def back_from_right_wall(set1, set2, t=3):
    """
    set1: レーザー測距センサー(前)の目標値
    set2: レーザー測距センサー(前)の目標値
    """
    start_t = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms, start_t) < t:
        d1 = get_mtof_distance(i2c1)
        d2 = get_mtof_distance(i2c2)
        print("d1:", d1)
        print("d2:", d2)

        if d1 is None or d2 is None:
            continue

        d12 = d1 - d2  # 目安は 30mm (で0.1くらいになるように)

        # 壁でなくターゲットとの距離を測ってしまった場合は何もしない
        if abs(d12) > 100:
            continue

        k1 = 0.1 / 30
        k2 = 0.1 / 30
        v1 = -k1 * (d1 - set1) + k2 * (d2 - set2)
        v2 = -k1 * (d1 - set1) + k2 * (d2 - set2)
        tire_l = -(1 + max(0, v2))
        tire_r = -(1 + max(0, v1))
        set_tire(tire_l, tire_r)


def set_tire_from_right_wall(set1, set2):
    """
    set1: レーザー測距センサー(前)の目標値
    set2: レーザー測距センサー(前)の目標値
    """
    global d12, dd12, sd12
    d1 = get_mtof_distance(i2c1)
    d2 = get_mtof_distance(i2c2)
    print("d1:", d1)
    print("d2:", d2)
    # while d1 is 8888:
    #     d1 = get_mtof_distance(i2c1)
    # while d2 is 8888:
    #     d2 = get_mtof_distance(i2c2)
    if d1 is None or d2 is None:
        return

    d12_ = d1 - d2  # 目安は 30mm (で0.1くらいになるように)

    # 壁でなくターゲットとの距離を測ってしまった場合は何もしない(一旦7.5cmとしている)
    if abs(d12_) > 100:
        print("abs(d12_) > 30    (return)")
        sd12 += d12 if d12 else 0
        return

    if d12 and abs(d12_ - d12) > 100:
        print("abs(dd12_) > 30    (return)")
        sd12 += d12 if d12 else 0
        return

    k1 = 0.1 / 30  # 壁との距離
    k2 = 0.1 / 30  # 壁との角度
    vl = k1 * ((d1 - set1) + (d2 - set2)) / 2 + k2 * (d1 - d2)
    vr = -k1 * ((d1 - set1) + (d2 - set2)) / 2 - k2 * (d1 - d2)
    # vl = k1 * (d1 - set1) + k2 * (d2 - set2)
    # vr = -k1 * (d1 - set1) - k2 * (d2 - set2)
    tire_l = 0.9 + vl
    tire_r = 0.9 + vr

    # sd12 += d12_
    # dd12 = d12_ - d12 if d12 else None
    # d12 = d12_

    # kp = 0.3 / 30
    # ki = kp * 0
    # kd = kp * 0
    # # ki = kp * 0.0001
    # # kd = kp * 0

    # v = kp * d12_ + ki * sd12 + (kd * dd12 if dd12 else 0)
    # tire_l = 1 - max(0, -v)
    # tire_r = 1 - max(0, v)
    # tire_l = 0.95 - kp * max(0, -d12)
    # tire_r = 1 - kp * max(0, d12)
    set_tire_left(tire_l)
    set_tire_right(tire_r)


# 一定距離進む関数
# def move_front(distance):
#     """
#     distance: [cm]
#     """
#     pass


# Uターンする関数
# Uターン時に、デフォルトの距離で壁にぶつかる場合はTrue、そうでない場合はFalseを返す。
# distance_to_go: 仮のデフォルト値。実際には、Uターンするために必要な距離を設定する。
# def u_turn_right(zigzag_offset=30):
#     """
#     distance_to_go: [cm]
#     """
#     global direction
#     turn_right()
#     move_front(zigzag_offset)
#     turn_right()
#     return zigzag_offset < 10  # 仮の閾値。


# def u_turn_left(distance_to_go=30):
#     """
#     distance_to_go: [cm]
#     """
#     global direction
#     turn_left()
#     move_front(distance_to_go)
#     turn_left()
#     return distance_to_go < 10  # 仮の閾値。


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


def set_tire_from_front_sw():
    l = is_left_arm_pressed()
    r = is_right_arm_pressed()
    # TODO: スピードの調整
    if not l and not r:
        set_tire(1, 1)
    elif l and not r:
        set_tire(0, 1)
    elif not l and r:
        set_tire(1, 0)
    # match l, r:
    #     case False, False:
    #         set_tire(1, 1)
    #     case True, False:
    #         set_tire(0, 1)
    #     case False, True:
    #         set_tire(1, 0)


def move_forward_and_back_while_target_in_catcher(loop_max=10, speed=0.8, t_forward=0.1, t_back=0.1):
    """
    loop_max: 最大の往復数
    """
    i = 0
    while is_catching() and i < loop_max:
        # set_tire(-speed, -speed)
        # time.sleep(t_back)
        # set_tire(speed, speed)
        # time.sleep(t_forward)

        set_tire(-0.6, -0.5, 1, 1)
        time.sleep(0.15)
        set_tire(0, 0)
        time.sleep(0.15)
        set_tire(0.95, 1, 1, 1)
        time.sleep(0.15)
        set_tire(0, 0)
        time.sleep(0.15)
        i += 1


def pivot_right_and_left_while_target_in_catcher(loop_max=10, speed=0.8, t=0.1):
    """
    loop_max: 最大の往復数
    """
    i = 0
    while is_catching() and i < loop_max:
        set_tire(-speed, speed)
        time.sleep(t)
        set_tire(speed, -speed)
        time.sleep(t)
        i += 1


correction_factor_l = 0.92
correction_factor_r = 1


def set_tire(val_l, val_r, correction_factor_l=correction_factor_l, correction_factor_r=correction_factor_r):
    """
    val_l, val_r: -1 ~ 1 の値
    """
    set_tire_left(val_l, correction_factor_l)
    set_tire_right(val_r, correction_factor_r)


def set_tire_left(val, correction_factor_l=correction_factor_l):
    """
    val: -1 ~ 1 の値
    """
    val = min(1, max(-1, val))
    val *= correction_factor_l
    if val < 0:
        pwm_motor_bin1.duty_u16(0)
        pwm_motor_bin2.duty_u16(math.floor(val * 65535))
        # pin_motor_bin1.value(0)
        # pin_motor_bin2.value(1)
    elif val == 0:
        pwm_motor_bin1.duty_u16(65535)
        pwm_motor_bin2.duty_u16(65535)
        # pin_motor_bin1.value(1)
        # pin_motor_bin2.value(1)
    else:
        pwm_motor_bin1.duty_u16(math.floor(val * 65535))
        pwm_motor_bin2.duty_u16(0)
        # pin_motor_bin1.value(1)
        # pin_motor_bin2.value(0)


def set_tire_right(val, correction_factor_r=correction_factor_r):
    """
    val: -1 ~ 1 の値
    """
    val = min(1, max(-1, val))
    val *= correction_factor_r
    if val < 0:
        pwm_motor_ain1.duty_u16(0)
        pwm_motor_ain2.duty_u16(math.floor(val * 65535))
        # pin_motor_ain1.value(1)
        # pin_motor_ain2.value(0)
    elif val == 0:
        pwm_motor_ain1.duty_u16(65535)
        pwm_motor_ain2.duty_u16(65535)
        # pin_motor_ain1.value(1)
        # pin_motor_ain2.value(1)
    else:
        pwm_motor_ain1.duty_u16(math.floor(val * 65535))
        pwm_motor_ain2.duty_u16(0)
        # pin_motor_ain1.value(0)
        # pin_motor_ain2.value(1)


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
        if is_catching():  # ターゲットがロールに入った場合
            # 停止し、しばらく待機 TODO: 停止時間の調整
            set_tire(0, 0)
            time.sleep(3)

            move_forward_and_back_while_target_in_catcher()
            pivot_right_and_left_while_target_in_catcher()

        set_tire_from_front_sw()


print("finish tire settings (in tire.py)")
