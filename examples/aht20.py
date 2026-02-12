# main.py - AHT20传感器读取（简化版）
import machine
import time
from ahtx0 import AHT20
# 1. 初始化I2C总线
i2c = machine.I2C(1, freq=400000)  # 使用I2C1
# 2. 扫描I2C设备
print("I2C设备扫描:")
devices = i2c.scan()
if devices:
    for addr in devices:
        print("地址: 0x" + hex(addr)[2:])
else:
    print("未找到I2C设备")
    # 停止程序
    import sys
    sys.exit()
# 3. 初始化AHT20传感器
sensor = AHT20(i2c)
print("AHT20初始化完成")

try:
    while True:
        # 读取温湿度
        temp = sensor.temperature
        hum = sensor.relative_humidity
        
        # 显示数据（简化输出）
        print("温度: %.1f°C" % temp)
        print("湿度: %.1f%%" % hum)
        print("-" * 20)
        
        # 等待2秒
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\n程序已停止")