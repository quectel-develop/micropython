from umqtt.robust import MQTTClient
import time

# MQTT连接配置
BROKER = '101.37.104.185'
PORT = 41990
USERNAME = 'quectel'
PASSWORD = '12345678'
CLIENT_ID = 'umqtt_client'
TOPIC = b'/a1vvrmkn43t/NiFtKoHMcu6j0VIXtC6e/user/get'

# 消息回调函数
def on_message(topic, msg):
    print(f'[Topic]   {topic.decode()}')
    print(f'[Message] {msg.decode()}')

# 创建MQTT客户端
client = MQTTClient(
    client_id = CLIENT_ID,
    server = BROKER,
    port = PORT,
    user = USERNAME,
    password = PASSWORD
)

# 设置消息回调
client.set_callback(on_message)

try:
    # 连接到服务器
    print(f'### Connecting to {BROKER}:{PORT}...')
    client.connect()
    print('### Connected successfully !')
    
    # 订阅所有主题
    client.subscribe(TOPIC)
    print('### Topic subscribed.')
    # 先进行一次publish
    try:
        client.publish(TOPIC, b'Hello from MQTT client !')
    except Exception as e:
        print(f'*** Subscribe failed. Err: {e}')
        
    # 持续监听消息
    while True:
        try:
            # 检查新消息（非阻塞）
            client.check_msg()
            time.sleep(0.1)  # 短暂延时
        except KeyboardInterrupt:
            print('\n### Interrupted.')
            break
        except Exception as e:
            print(f'*** Recv Err: {e}')
            
except Exception as e:
    print(f'*** Connect failed. Err: {e}')
    
finally:
    # 断开连接
    try:
        client.disconnect()
        print('### Disconnected.')
    except:
        pass
