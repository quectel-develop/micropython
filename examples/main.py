import machine
import time

led_red = machine.Pin('LED_RED', machine.Pin.OUT)
while True:
    print('Hello World !')
    led_red.value(1)
    time.sleep(0.5)
    led_red.value(0)
    time.sleep(0.5)