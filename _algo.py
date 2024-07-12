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
def go(distance):
    """
    distance: [cm]
    """
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
    go(zigzag_offset)
    turn_right()
    return zigzag_offset < 10  # 仮の閾値。


def u_turn_left(distance_to_go=30):
    """
    distance_to_go: [cm]
    """
    global direction
    turn_left()
    go(distance_to_go)
    turn_left()
    return distance_to_go < 10  # 仮の閾値。


# 移動方向を設定する関数
def set_direction(dir):
    """
    direction: "forward", "right", "left", "stop" のいずれか
    """
    pass


# 各種センサーにより状態を得る関数
def is_front_close_to_wall():
    pass


def is_right_arm_pressed():
    pass


def is_left_arm_pressed():
    pass


def is_close_to_right_wall():
    pass


def is_close_to_left_wall():
    pass


def is_target_in_roll():
    pass


def is_target_detected():
    pass


def distance_to_front():
    return 0  # 仮の値。実際にはセンサーで取得する。


def is_direction_north():
    return True  # 実際にはセンサーの値を元に判断する。


# 動作をまとめた関数
def go_to_wall_with_target_collection():
    while not is_front_close_to_wall():
        if is_target_in_roll():  # ターゲットがロールに入った場合
            # 停止し、ターゲットを回収し終えるまで待つ
            set_direction("stop")
            while is_target_in_roll():
                continue
            continue

        # アームの押され方によって進む方向を決定する(壁にぶつかっている状態 or ターゲット(か壁)が左右のにぶつかっている状態 or 何もない状態)
        match is_right_arm_pressed(), is_left_arm_pressed():
            case True, True:
                pass  # ルール的にはありえない。もしくは壁にぶつかったことをこれで判定するか。
            case True, False:
                set_direction("right")
            case False, True:
                set_direction("left")
            case False, False:
                # 単に前進...できれば、現在次の壁に到達するまでに保つべき壁との距離を保持しておいて「壁との距離を保ちながら前進」
                set_direction("forward")


# 定数
zigzag_offset = 20  # Uターン時に左右にずれる距離（仮の値）。
zigzag_threshold = 10  # Uターン時に左右にずれる距離がこの値より小さい場合、Uターンできないと判定する。

# ----------------- ここからメイン処理 -----------------

# 初期条件
direction = "W"


# ZONE1
go_to_wall_with_target_collection()
turn_right()
go(30)
turn_right()

go_to_wall_with_target_collection()
turn_left()
go(30)
turn_left()

go_to_wall_with_target_collection()
turn_right()
go(50)
# ここで SAVE POINT に到着


# ZONE2
# 少し進んで右(=東)を向く
go(20)
turn_right()

# まず、ある程度ターゲットを回収するために、ジグザグしながらゴールまで進む
# このループを抜けるときには、ゴール地点で東側を向いた状態になる。
while True:
    go_to_wall_with_target_collection()

    # 壁にぶつかった場合ここに来る
    if direction == "W":
        turn_right()
        if distance_to_front() < zigzag_threshold:
            # 北側の壁に到着。
            # ゴール地点に移動するための特別の処理をする
            go_to_wall_with_target_collection()  # とりあえず壁まで移動
            turn_right()  # ゴール地点を向く
            go_to_wall_with_target_collection()  # ゴール地点まで移動
            break
        go(zigzag_offset)
        turn_right()
    else:
        turn_left()
        if distance_to_front() < zigzag_threshold:
            # 北側の壁に到着。
            # ゴール地点に移動するための特別の処理をする
            go_to_wall_with_target_collection()  # とりあえず壁まで移動
            turn_right()  # ゴール地点を向く
            break
        go(zigzag_offset)
        turn_left()


# 一度、ある程度ターゲットを回収しつつゴールまでたどり着いたらここに来る。
# 今度はフィールドを1周しながらターゲットが残っていないかチェックし、あれば回収する。
# 左側に壁がある状態で1周する。
while True:
    has_found_target_this_cycle = False

    # ゴール地点に来るまで、フィールドを1周する。（壁にぶつかったとき、東を向いていれば1周したことになる。）
    while direction != "E":
        # 壁にぶつかるまで前進。ただし右側にターゲットを発見した場合は回収する。
        while not is_front_close_to_wall():
            if is_target_detected():
                has_found_target_this_cycle = True
                turn_right()
                go_to_wall_with_target_collection()
                break
            set_direction("forward")
        # 壁にぶつかったら右に曲がる
        turn_right()

    if not has_found_target_this_cycle:
        break

# これで、全てのターゲットを回収し終えた状態で、ゴール地点に向いていることが保証される。


# 検討事項
# - 壁にぶつかるのをどう判定するか。センサーを前側に付けるか否か。壁に対して平行であることをどう保証するか。ボタンで判定できそうかもしれない。
# - ターゲット回収後、壁にぶつかるまで前進するのか、来た道を引き返すのか。（特に、フィールドを1周するフェーズで）
