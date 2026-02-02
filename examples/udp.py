import usocket as socket

# 创建TCP套接字
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(socket.getaddrinfo('www.baidu.com',80))

# 发送消息并接收回应
while True:
    # 获取用户输入
    msg = input("发送: ")
    
    # 如果用户输入exit则退出
    if msg.lower() == 'exit':
        break
    # 发送消息
    client.sendto(msg.encode(), ('101.37.104.185', 41318))
    
    # 接收服务器回应
    response = client.recvfrom(1024)
    print("服务器回应:", response)
    

# 关闭连接
client.close()
print("连接已关闭")
