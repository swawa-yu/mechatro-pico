from machine import Pin, PWM

print("init pin settings (in pin.py)")

# マイクロスイッチ
pin_front_sw_l = Pin(0, Pin.IN, Pin.PULL_DOWN)  # 1
pin_front_sw_r = Pin(1, Pin.IN, Pin.PULL_DOWN)  # 2

# モーター
pin_motor_ain1 = Pin(2, Pin.OUT)  # 4
pin_motor_ain2 = Pin(3, Pin.OUT)  # 5
pin_motor_bin1 = Pin(4, Pin.OUT)  # 6
pin_motor_bin2 = Pin(5, Pin.OUT)  # 7

pwm_motor_ain1 = PWM(pin_motor_ain1)
pwm_motor_ain2 = PWM(pin_motor_ain2)
pwm_motor_bin1 = PWM(pin_motor_bin1)
pwm_motor_bin2 = PWM(pin_motor_bin2)

pwm_motor_ain1.freq(200000)
pwm_motor_ain2.freq(200000)
pwm_motor_bin1.freq(200000)
pwm_motor_bin2.freq(200000)

# レーザー測距センサー
pin_mtof1_sda = Pin(6)  # 9 黄
pin_mtof1_scl = Pin(7)  # 10 緑
pin_mtof2_sda = Pin(8)  # 11 黄
pin_mtof2_scl = Pin(9)  # 12 緑

# 超音波測距センサー
# 提出物①の情報と異なるので注意
pin_front_hcsr_trig = Pin(20, Pin.OUT)  # 26 黄
pin_front_hcsr_echo = Pin(21, Pin.IN)  # 27 緑
pin_right_hcsr_trig = Pin(26, Pin.OUT)  # 31 黄
pin_right_hcsr_echo = Pin(27, Pin.IN)  # 32 緑

# キャッチャー用センサー
pin_catcher_sw = Pin(13, Pin.IN, Pin.PULL_DOWN)

# リモコン
pin_rimocon_sw_left1 = Pin(16, Pin.IN, Pin.PULL_DOWN)
pin_rimocon_sw_left2 = Pin(17, Pin.IN, Pin.PULL_DOWN)
pin_rimocon_sw_right1 = Pin(18, Pin.IN, Pin.PULL_DOWN)
pin_rimocon_sw_right2 = Pin(19, Pin.IN, Pin.PULL_DOWN)


print("finish pin settings (in pin.py)")
