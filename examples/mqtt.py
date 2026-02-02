from umqtt.robust import MQTTClient
import time

# MQTT连接配置
BROKER = "101.37.104.185"
PORT = 45468
USERNAME = "quectel"
PASSWORD = "12345678"
CLIENT_ID = "umqtt_client"

# 消息回调函数
def on_message(topic, msg):
    print(f"主题: {topic.decode()}")
    print(f"消息: {msg.decode()}")

# 创建MQTT客户端
client = MQTTClient(
    client_id=CLIENT_ID,
    server=BROKER,
    port=PORT,
    user=USERNAME,
    password=PASSWORD
)

# 设置消息回调
client.set_callback(on_message)

try:
    # 连接到服务器
    print(f"正在连接到 {BROKER}:{PORT}...")
    client.connect()
    print("连接成功!")
    
    # 订阅所有主题
    client.subscribe(b"/a1vvrmkn43t/NiFtKoHMcu6j0VIXtC6e/user/get")
    print("已订阅")
        # 添加一次publish操作
    publish_message = b"Hello from MQTT client!"
    try:
        client.publish(b"/a1vvrmkn43t/NiFtKoHMcu6j0VIXtC6e/user/get", publish_message)
    except Exception as e:
        print(f"⚠️ 发布消息失败: {e}")
    # 持续监听消息
    while True:
        try:
            # 检查新消息（非阻塞）
            client.check_msg()
            time.sleep(0.1)  # 短暂延时
        except KeyboardInterrupt:
            print("\n手动中断")
            break
        except Exception as e:
            print(f"接收消息错误: {e}")
            
except Exception as e:
    print(f"连接错误: {e}")
    
finally:
    # 断开连接
    try:
        client.disconnect()
        print("已断开连接")
    except:
        pass
