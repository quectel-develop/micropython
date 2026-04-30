import machine
import time

def uart_basic():
    """基础串口示例"""
    
    # 初始化串口2 (USART2)
    uart2 = machine.UART(2, 9600)
    
    print("UART2 初始化完成，等待数据...")
    
    while True:
        
        # 2. 检查是否有数据接收
        if uart2.any():
            # 读取接收到的数据
            data = uart2.read()
            if data:
                print(f"receive: {data}")
                print(len(data))
                # 回显数据
                uart2.write(data)
        
        time.sleep(0.1)

total = 0
def uart_irq():
    def uart_rx_handler(uart_obj):
        global total
        """UART接收中断处理函数"""
        count = uart_obj.any()
        if count:
            data = uart_obj.read(count)
            print(f"receive: {data}")
            total += count
            print(f"total {total}")

    # 配置UART
    uart = machine.UART(2, 9600, rxbuf=256)

    # 配置接收中断
    uart.irq(handler=uart_rx_handler, trigger=machine.UART.IRQ_RX)


    while True:
        machine.idle()  # 进入低功耗模式，等待中断
#uart_basic()
uart_irq()