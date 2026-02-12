import usys as sys
import uos as os
import utime as time
from ftplib import FTP

HOST = '112.31.84.164'
PORT = 8309
USERNAME = 'test'
PASSWORD = 'GJbMlzZB65'
WORKDIR = '/UniKnect'
TIMEOUT = 30

remote_file = 'hello.txt'
local_file = 'hello_dl.txt'


if __name__ == "__main__":
    print('\n### Test start.')
    print('=' * 50)
    
    try:
        # 创建连接
        ftp = FTP()
        ftp.connect(HOST, PORT, TIMEOUT)
        welcome = ftp.login(USERNAME, PASSWORD)
        print(f'### Welcome: {welcome}\n')
        
        
        # 切换目录
        try:
            ftp.cwd(WORKDIR)
            print(f'### Change to {WORKDIR}\n')
        except:
            print(f'*** Change to {WORKDIR} failed, use root directory.\n')
        
        
        # 上传文件
        with open('hello.txt', 'w') as f:
            f.write('This is a FTP test.')
        
        with open('hello.txt', 'rb') as f:
            ftp.storbinary(f'STOR {remote_file}', f)
        print('\n### Upload file done !')
        
        
        # 文件列表
        files = ftp.nlst()
        print('\n### File List:')
        for f in files:
            print(f"\t{f}")
        
        
        # 下载文件
        with open(local_file, 'wb') as f:
            def callback(data):
                f.write(data)
            ftp.retrbinary(f'RETR {remote_file}', callback)
        print('\n### Download file done !')
    
    
        # 验证下载
        with open(local_file, 'rb') as f:
            content = f.read().decode('utf-8')
            print(f'### Content: {content}')
        
        
        # 断开连接
        ftp.quit()
        
    except Exception as e:
        print(f"Error: {e}")
    