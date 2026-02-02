import usocket

# 最简单直接的实现
s = usocket.socket()
s.connect(("101.37.104.185", 43630))

# 发送HTTP GET请求
#s.send("1111".encode())
s.send(b"1 /1024.txt HTTP/1.0\r\nHost: 112.31.84.164:8300\r\nConnection: close\r\n\r\n")
# 接收响应
data = b""
while True:
    chunk = s.recv(1024)
    data += chunk
    break

s.close()

# 输出响应
print("response:", data.decode())