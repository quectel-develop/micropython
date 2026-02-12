import machine
import time
import random
from st7735 import LCD
# 初始化SPI
spi = machine.SPI(1, baudrate=40000000, polarity=0, phase=0)
lcd = LCD(spi, dc_pin="F12", cs_pin="D14")
lcd.set_rotation(1)
# 模拟传感器数据
def get_sensor_data():
    # 模拟ADC电压 (0-3.3V)
    voltage = random.uniform(3.0, 3.5)
    # 模拟温度湿度
    temp = random.uniform(20.0, 30.0)
    humi = random.uniform(40.0, 60.0)
    return voltage, temp, humi

# 主显示函数
def sensor_display():
    # 清屏
    lcd.fill_screen(lcd.BLACK)
    
    # 显示固定标题
    lcd.show_string(0, 6, "Voltage", lcd.BLUE, lcd.BLACK)
    lcd.show_string(0, 46, "Temp/Humi", lcd.BLUE, lcd.BLACK)
    
    print("Sensor test start.")
    
    while True:
        # 获取数据
        voltage, temp, humi = get_sensor_data()
        
        # 打印到串口
        print(f"--### Voltage:        {voltage:.2f}V")
        print(f"--### Temp/Humi:      {temp:.1f}C / {humi:.1f}%")
        
        
        # 显示电压
        voltage_str = f"{voltage:.2f}V"
        lcd.show_string(0, 26, voltage_str, lcd.WHITE)
        
        # 显示温湿度
        temp_humi_str = f"{temp:.1f}C / {humi:.1f}%"
        lcd.show_string(0, 66, temp_humi_str, lcd.WHITE, lcd.BLACK)
        lcd.flush()
        # 1秒刷新
        time.sleep(1)

# 运行
sensor_display()