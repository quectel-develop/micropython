from machine import ADC, Pin
import time

# 初始化ADC
ldr = ADC(Pin('C5'))  # 对应您的 ADC_CHANNEL_15, PC5

# 正确的方法：使用 read_u16()
def get_adc():
    return ldr.read_u16()  # 返回 0-65535

# 转换为12位（STM32是12位ADC）
def get_adc_12bit():
    """转换为12位值 (0-4095)"""
    value_16bit = ldr.read_u16()  # 0-65535
    # 右移4位，16位转12位
    value_12bit = value_16bit >> 4
    return value_12bit & 0xFFF  # 确保范围在0-4095

# 转换为电压
def get_voltage():
    """读取并转换为电压值"""
    value = get_adc_12bit()
    return (value * 3.3) / 4095.0

# 测试所有方法
print("测试ADC读取...")
print("=" * 40)

while True:
    # 方法1: 直接读取
    raw_u16 = ldr.read_u16()
    
    # 方法2: 12位值
    raw_12bit = get_adc_12bit()
    
    # 方法3: 电压值
    voltage = get_voltage()
    
    print(f"read_u16: {raw_u16:5d} | 12-bit: {raw_12bit:4d} | Voltage: {voltage:.2f}V")
    time.sleep(1)