from umqtt.robust import MQTTClient
import time
import tls
import sys

# MQTT连接配置
BROKER = "101.37.104.185"
PORT = 40579
USERNAME = "quectel"
PASSWORD = "12345678"
CLIENT_ID = "umqtt_client"
TOPIC = b"/a1vvrmkn43t/NiFtKoHMcu6j0VIXtC6e/user/get"
PUBLISH_TOPIC = b"/a1vvrmkn43t/NiFtKoHMcu6j0VIXtC6e/user/update"
CA_CERT_PATH = '/flash/mqtt_ca.cer'

# 读取证书文件内容
def read_cert_file(filepath):
    """读取证书文件，如果失败则退出程序"""
    try:
        # 先尝试文本模式读取
        with open(filepath, 'r') as f:
            content = f.read()
            print(f"✅ 成功读取证书文件: {filepath}")
            return content
    except FileNotFoundError:
        print(f"❌ 错误: 证书文件不存在: {filepath}")
        sys.exit(1)
    except PermissionError:
        print(f"❌ 错误: 没有权限读取证书文件: {filepath}")
        sys.exit(1)
    except Exception as e:
        # 尝试二进制读取
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
                # 尝试解码为字符串
                try:
                    content = content.decode('utf-8')
                except:
                    # 保持二进制格式
                    pass
                print(f"✅ 成功读取证书文件(二进制模式): {filepath}")
                return content
        except Exception as e2:
            print(f"❌ 错误: 读取证书文件失败 {filepath}: {e2}")
            sys.exit(1)

# 消息回调函数
def on_message(topic, msg):
    print(f"主题: {topic.decode()}")
    print(f"消息: {msg.decode()}")

# 读取证书内容
ca_content = read_cert_file(CA_CERT_PATH)

# 创建SSL上下文
context = tls.SSLContext(tls.PROTOCOL_TLS_CLIENT)
context.verify_mode = tls.CERT_REQUIRED

# 加载证书
if isinstance(ca_content, str):
    ca_content = ca_content.encode('utf-8')

try:
    # 尝试使用cadata加载证书
    context.load_verify_locations(ca_content)
    print("✅ SSL上下文配置成功")
except TypeError:
    print(f"❌ 错误: 加载证书失败")
    sys.exit(1)

# 创建MQTT客户端
try:
    client = MQTTClient(
        client_id=CLIENT_ID,
        server=BROKER,
        port=PORT,
        user=USERNAME,
        password=PASSWORD,
        ssl=context  # 直接传入SSL上下文
    )
except Exception as e:
    print(f"❌ 错误: 创建MQTT客户端失败: {e}")
    sys.exit(1)

# 设置消息回调
client.set_callback(on_message)

try:
    # 连接到服务器
    print(f"正在连接到 {BROKER}:{PORT}...")
    client.connect()
    print("✅ 连接成功!")
    
    # 订阅主题
    client.subscribe(TOPIC)
    print("✅ 已订阅")
    
    # 添加一次publish操作
    publish_message = b"Hello from MQTT client!"
    try:
        client.publish(PUBLISH_TOPIC, publish_message)
        print(f"✅ 已发布消息到主题: {PUBLISH_TOPIC.decode()}")
        print(f"📤 消息内容: {publish_message.decode()}")
    except Exception as e:
        print(f"⚠️ 发布消息失败: {e}")
    
    # 持续监听消息
    print("\n开始监听消息... (按Ctrl+C退出)")
    while True:
        try:
            # 检查新消息（非阻塞）
            client.check_msg()
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n手动中断")
            break
        except Exception as e:
            print(f"接收消息错误: {e}")
            
except Exception as e:
    print(f"❌ 连接错误: {e}")
    
finally:
    # 断开连接
    try:
        client.disconnect()
        print("✅ 已断开连接")
    except:
        pass