import machine
import time

# 初始化I2C
i2c = machine.I2C(1, freq=100000) 

print("I2C初始化完成")

# AHT20的固定地址
AHT20_ADDR = 0x38

# 1. 发送初始化命令
print("\n1. 发送初始化命令...")
count = i2c.writeto(AHT20_ADDR, b'\xBE\x08\x00')  # 初始化命令
time.sleep_ms(10)

# 2. 发送触发测量命令
print("2. 发送触发测量命令...")
i2c.writeto(AHT20_ADDR, b'\xAC\x33\x00')  # 触发测量
time.sleep_ms(80)  # 等待测量完成

# 3. 读取6字节数据 - 使用readfrom_into
print("3. 读取数据...")
data_buf = bytearray(6)  # 创建缓冲区
i2c.readfrom_into(AHT20_ADDR, data_buf)  # 读取到缓冲区
print(f"  原始数据: {data_buf.hex(' ')}")

# 4. 解析温湿度
# 数据格式: [状态, 湿度(20bit), 温度(20bit)]
humidity_raw = ((data_buf[1] << 12) | (data_buf[2] << 4) | (data_buf[3] >> 4))
temperature_raw = (((data_buf[3] & 0x0F) << 16) | (data_buf[4] << 8) | data_buf[5])

# 转换公式
humidity = (humidity_raw * 100) / 0x100000  # 0-100%
temperature = ((temperature_raw * 200.0) / 0x100000) - 50  # -50~+150°C

print(f"\n温度: {temperature:.1f}°C")
print(f"湿度: {humidity:.1f}%")
