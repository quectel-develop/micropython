# main.py - 主程序文件
import machine
import time
from st7735 import LCD
from images import QQ_ICON_40x40

def main():
    # 1. 初始化SPI
    spi = machine.SPI(1, baudrate=20000000, polarity=0, phase=0)
    
    # 2. 初始化LCD
    lcd = LCD(spi, dc_pin="F12", cs_pin="D14")
    lcd.set_rotation(2)
    # 3. 清屏
    lcd.fill_screen(lcd.BLACK)
    lcd.flush()
    time.sleep(1)
    
    # 4. 显示QQ图标在左上角
    print("显示QQ图标 (40x40)...")
    lcd.show_image(0, 0, 40, 40, QQ_ICON_40x40)
    lcd.flush()
    time.sleep(2)
    
    # 5. 清除图标区域
    print("清除图标区域...")
    lcd.fill_rectangle(0, 0, 40, 40, lcd.BLACK)
    lcd.flush()
    time.sleep(1)
    
    # 6. 在屏幕中央显示QQ图标
    print("在屏幕中央显示QQ图标...")
    center_x = (lcd.WIDTH - 40) // 2
    center_y = (lcd.HEIGHT - 40) // 2
    lcd.show_image(center_x, center_y, 40, 40, QQ_ICON_40x40)
    lcd.flush()
    time.sleep(2)
    
    # 7. 显示多个图标
    print("显示多个图标...")
    
    # 左上角
    lcd.show_image(10, 10, 40, 40, QQ_ICON_40x40)
    
    # 右上角
    lcd.show_image(lcd.WIDTH - 50, 10, 40, 40, QQ_ICON_40x40)
    
    # 左下角
    lcd.show_image(10, lcd.HEIGHT - 50, 40, 40, QQ_ICON_40x40)
    
    # 右下角
    lcd.show_image(lcd.WIDTH - 50, lcd.HEIGHT - 50, 40, 40, QQ_ICON_40x40)
    
    lcd.flush()
    time.sleep(3)
    
    # 8. 清除屏幕
    print("清除屏幕...")
    lcd.fill_screen(lcd.BLACK)
    lcd.flush()
    
    # 9. 创建动画效果
    print("创建动画效果...")
    for i in range(0, lcd.WIDTH - 40, 5):
        # 清除旧位置
        if i > 0:
            lcd.fill_rectangle(i-5, 50, 40, 40, lcd.BLACK)
        
        # 绘制新位置
        lcd.show_image(i, 50, 40, 40, QQ_ICON_40x40)
        lcd.flush()
        time.sleep_ms(50)
    
    # 10. 显示文本和图标组合
    print("显示文本和图标组合...")
    lcd.fill_screen(lcd.WHITE)
    
    # 显示标题
    lcd.show_string(10, 10, "QQ Icon Demo", lcd.RED, lcd.WHITE, 16)
    
    # 显示图标
    lcd.show_image(60, 40, 40, 40, QQ_ICON_40x40)
    
    # 显示说明文字
    lcd.show_string(20, 90, "40x40 RGB565", lcd.BLUE, lcd.WHITE, 12)
    lcd.show_string(20, 110, "3200 bytes", lcd.GREEN, lcd.WHITE, 12)
    
    lcd.flush()
    
    print("演示完成!")

if __name__ == "__main__":
    main()