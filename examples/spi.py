import machine

# 创建SPI对象
spi = machine.SPI(1, baudrate=2000000, bits=8)

# 发送数据
spi.write(b'\x01\x02\x03')

# 读取数据
#data = spi.read(10)
data = spi.read(10, 0x1f)
print(data)