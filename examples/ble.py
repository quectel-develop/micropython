import utime
from quectel import BLE
import _thread
import machine
from ahtx0 import AHT20
# =========================
# 全局常量
# =========================
CUSTOM_SERV_ID = 0
CUSTOM_CHAR_ID = 0
CUSTOM_CHAR_ID1 = 1

CUSTOM_SERVICE_UUID = 0xFFF0
CUSTOM_CHAR_UUID = 0xFFF1
CUSTOM_CHAR_UUID1 = 0xFFF2
CCCD_UUID = 0x2902

# =========================
# 全局状态
# =========================
g_ble_connected = False
g_notify_enabled = False
g_notify_thread_running = False


def str_to_hex(s):
    return ''.join(['%02X' % b for b in s.encode()])


def notify_task(ble, semaphore):
    global g_ble_connected
    global g_notify_enabled
    global g_notify_thread_running
    i2c = machine.I2C(1, freq=400000)
    devices = i2c.scan()
    sensor = AHT20(i2c)
    while g_notify_thread_running:
        try:
            if g_ble_connected and g_notify_enabled:
                temp = sensor.temperature
                temp_str = "{:.1f}".format(temp)
                hum = sensor.relative_humidity
                hum_str = "{:.1f}".format(hum)
                ble.notify(CUSTOM_CHAR_UUID, len(temp_str), temp_str)
                print("notify send:", temp_str)
                ble.indicate(CUSTOM_CHAR_UUID1, len(hum_str), hum_str)
                print("indicate send:", hum_str)
            utime.sleep(1)

        except Exception as e:
            print("notify error:", e)
            utime.sleep(1)
    print("notify thread exit")
    semaphore.release()


def cb(evt):
    global g_ble_connected
    global g_notify_enabled
    print("evt =", evt)

    if evt["event"] == BLE.EVT_CONNECTED:
        g_ble_connected = True
        print("connected")

    elif evt["event"] == BLE.EVT_DISCONNECTED:
        g_ble_connected = False
        g_notify_enabled = False
        print("disconnected")

    elif evt["event"] == BLE.EVT_MTU:
        print("mtu =", evt["mtu"])

    elif evt["event"] == BLE.EVT_VAL_DATA:
        print("ch uuid =", hex(evt["uuid"]), "value =", evt["value"])
    elif evt["event"] == BLE.EVT_DESCDATA:
        print("ch uuid =", hex(evt["uuid"]),
              "desc uuid =", hex(evt["desc_uuid"]),
              "value =", evt["value"])

        if evt["desc_uuid"] == CCCD_UUID and evt["uuid"] == CUSTOM_CHAR_UUID:
            val = str(evt["value"]).upper()

            if val == "0100":
                g_notify_enabled = True
                print("notify enabled")

            elif val == "0200":
                g_notify_enabled = False
                print("indicate enabled (not using notify now)")

            elif val == "0000":
                g_notify_enabled = False
                print("notify disabled")


def main():
    global g_notify_thread_running

    started = False
    
    ble = BLE()
    try:
        ok = ble.init(cb)
        if not ok:
            print("BLE init failed")
            return
        ble.set_dataformat(BLE.DATAFMT_STRING)

        ble.start("BLE_DEMO")
        started = True
        print("BLE base started")
        
        print(ble.get_addr())
        ble.add_service(CUSTOM_SERV_ID, CUSTOM_SERVICE_UUID, True)

        props = (BLE.PROP_READ | BLE.PROP_WRITE | BLE.PROP_NOTIFY | BLE.PROP_INDICATE)

        ble.add_character(CUSTOM_SERV_ID, CUSTOM_CHAR_ID, props, CUSTOM_CHAR_UUID)
        ble.set_character_value(
            CUSTOM_SERV_ID,
            CUSTOM_CHAR_ID,
            BLE.PERM_READ | BLE.PERM_WRITE,
            CUSTOM_CHAR_UUID,
            244,
            str_to_hex("1234")
        )
        ble.add_descriptor(
            CUSTOM_SERV_ID,
            CUSTOM_CHAR_ID,
            BLE.PERM_READ | BLE.PERM_WRITE,
            CCCD_UUID,
            "0000"
        )

        ble.add_character(CUSTOM_SERV_ID, CUSTOM_CHAR_ID1, props, CUSTOM_CHAR_UUID1)
        ble.set_character_value(
            CUSTOM_SERV_ID,
            CUSTOM_CHAR_ID1,
            BLE.PERM_READ | BLE.PERM_WRITE,
            CUSTOM_CHAR_UUID1,
            244,
            str_to_hex("4567")
        )
        ble.add_descriptor(
            CUSTOM_SERV_ID,
            CUSTOM_CHAR_ID1,
            BLE.PERM_READ | BLE.PERM_WRITE,
            CCCD_UUID,
            "0000"
        )

        ble.advertise()
        print("Advertising started, device name = QuecDemo")
        print("Press Ctrl+C to stop BLE...")

        # 启动通知线程
        g_notify_thread_running = True
        semaphore = _thread.allocate_semaphore(0)
        _thread.stack_size(4096)
        _thread.start_new_thread(notify_task, (ble,semaphore))
        while True:
            utime.sleep(1)

    except KeyboardInterrupt:
        print("\nCtrl+C detected, stopping BLE...")

    except Exception as e:
        print("BLE runtime error:", e)

    finally:
        # 先通知线程退出
        g_notify_thread_running = False
        semaphore.acquire(2000)

        if started:
            try:
                ble.stop()
                print("BLE stopped")
            except Exception as e:
                print("BLE stop failed:", e)

        try:
            ble.deinit()
            print("BLE deinitialized")
        except Exception as e:
            print("BLE deinit failed:", e)


main()
