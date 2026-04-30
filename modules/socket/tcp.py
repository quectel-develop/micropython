import usocket as socket
import sys

# 创建TCP套接字
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接服务器
try:
    client.connect(('101.37.104.185', 40078))
    print('##### Connected to server. #####')
except Exception as e:
    client.close()
    sys.exit()

# 发送消息并接收回应
while True:
    # 获取用户输入
    msg = input('[Send]')
    
    # 如果用户输入exit则退出
    if msg.lower() == 'exit':
        break
    if msg.strip() == '':
        continue
    # 发送消息
    client.send(msg.encode())
    
    # 接收服务器回应
    response = client.recv(1024)
    print('[Echo]', response)
    
# 关闭连接
client.close()
print('##### Disconnected to server. #####')