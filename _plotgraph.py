import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    port_list = []
    for port in ports:
        port_list.append(port.device)
    return port_list


def select_serial_port():
    while True:
        ports = list_serial_ports()
        if not ports:
            print("No serial ports found")
            return None
        print("Available serial ports:")
        for i, port in enumerate(ports):
            print(f"{i}: {port}")
        index = int(input("Select a serial port: "))
        if 0 <= index < len(ports):
            return ports[index]
        else:
            print("Invalid selection. Try again.")


# シリアルポートの選択
port = select_serial_port()
if port is None:
    exit()

# シリアルポートの設定
try:
    ser = serial.Serial(port, 115200)
except serial.SerialException as e:
    print(f"Failed to open serial port {port}: {e}")
    exit()

# データを格納するリスト
data1 = []
data2 = []

# グラフの設定
fig, (ax1, ax2) = plt.subplots(2, 1)
(line1,) = ax1.plot(data1, label="Sensor 1")
(line2,) = ax2.plot(data2, label="Sensor 2")
ax1.set_ylim(0, 1000)  # 距離センサの範囲に応じて調整
ax2.set_ylim(0, 1000)  # 距離センサの範囲に応じて調整
ax1.set_xlim(0, 100)
ax2.set_xlim(0, 100)
ax1.legend()
ax2.legend()


def update(frame):
    line1.set_ydata(data1)
    line1.set_xdata(range(len(data1)))
    line2.set_ydata(data2)
    line2.set_xdata(range(len(data2)))
    if len(data1) > 100:
        ax1.set_xlim(len(data1) - 100, len(data1))
    else:
        ax1.set_xlim(0, 100)
    if len(data2) > 100:
        ax2.set_xlim(len(data2) - 100, len(data2))
    else:
        ax2.set_xlim(0, 100)
    return line1, line2


def animate(i):
    try:
        line = ser.readline().decode("utf-8").strip()
        print(f"Received: {line}")  # デバッグ用に受信したデータを出力
        distance1, distance2 = map(int, line.split(":")[1].split())
        # if line.startswith("Distance1:"):
        #     distance1 = int(line.split(":")[1].strip())
        #     data1.append(distance1)
        #     if len(data1) > 100:
        #         data1.pop(0)
        # elif line.startswith("Distance2:"):
        #     distance2 = int(line.split(":")[1].strip())
        #     data2.append(distance2)
        #     if len(data2) > 100:
        #         data2.pop(0)
        data1.append(distance1)
        data2.append(distance2)
        if len(data1) > 100:
            data1.pop(0)
        if len(data2) > 100:
            data2.pop(0)
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except ValueError as e:
        print(f"Value error: {e}")  # デバッグ用に追加
    except:
        print("error")

    return update(i)


ani = animation.FuncAnimation(fig, animate, interval=100, cache_frame_data=False)
plt.show()
