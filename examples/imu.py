# main.py - 同时读取AHT20和LIS2DH12
import machine
import time
from lis2dh12 import LIS2DH12

# 初始化I2C
i2c = machine.I2C(1, freq=400000)

# 初始化LIS2DH12
lis2dh = LIS2DH12(i2c) 
print("LIS2DH12 就绪")

# 主循环
while True:
    
    # 读取加速度
    acc_x, acc_y, acc_z = lis2dh.acceleration
    
    # 显示结果
    print("加速度 X:{:+.3f} Y:{:+.3f} Z:{:+.3f} m/s²".format(acc_x, acc_y, acc_z))
    print("---")
    
    time.sleep(1)