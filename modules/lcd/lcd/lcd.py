# main.py - 主程序文件
import machine
import time
from st7735 import LCD
from images1 import Quectel_Icon_160x20

def main():
    # 1. 初始化SPI
    spi = machine.SPI(1, baudrate=20000000, polarity=0, phase=0)
    
    # 2. 初始化LCD
    lcd = LCD(spi, dc_pin="F12", cs_pin="D14")
    lcd.set_rotation(1)
    # 3. 清屏
    lcd.fill_screen(lcd.BLACK)
    
    # 4. 显示QQ图标在左上角
    print("显示Quectel图标 (160x20)...")
    lcd.show_image(0, 54, 160, 20, Quectel_Icon_160x20)
    lcd.flush()
    
    print("演示完成!")

if __name__ == "__main__":
    main()

