#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MicroPython FTP客户端脚本
适用于嵌入式设备
服务器: 112.31.84.164:8309
账号: test
密码: GJbMlzZB65
工作目录: /TEST
"""

try:
    import usys as sys
except ImportError:
    import sys

try:
    import uos as os
except ImportError:
    import os

try:
    import utime as time
except ImportError:
    import time

# 假设ftplib已经在设备上可用
# 或者通过以下方式导入
try:
    from ftplib import FTP
    from ftplibtls import FTP_TLS
except ImportError:
    # 如果ftplib不在标准位置，可能需要调整
    print("警告: 无法导入ftplibtls模块")
    # 尝试从当前目录导入
    try:
        sys.path.append('.')  # 添加当前目录到路径
        from ftplib import FTP
    except ImportError:
        print("错误: 需要ftplibtls模块")
        raise

# 读取证书文件内容
def read_cert_file(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except:
        try:
            with open(filepath, 'rb') as f:
                return f.read()
        except Exception as e:
            print(f"读取证书文件失败 {filepath}: {e}")
            return None

class MicroFTPClient:
    def __init__(self, host, port, username, password, workdir='/FTP-TEST'):
        """
        MicroPython FTP客户端初始化
        
        参数:
            host: FTP服务器地址
            port: FTP服务器端口
            username: 用户名
            password: 密码
            workdir: 工作目录
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.workdir = workdir
        self.ftp = None
        self.connected = False
    
    def connect(self, timeout=30):
        """连接到FTP服务器"""
        try:
            print(f"正在连接到 {self.host}:{self.port}...")
            
            # 创建FTP连接
            ca_content = read_cert_file('/flash/ftp_ca.pem')
            # 2. 配置SSL参数
            ssl_params = {
                "ca": ca_content,          # CA证书内容
                "session_reuse": True,     # 控制通道会话是否复用
            }
            self.ftp = FTP_TLS(ssl_params=ssl_params)
            #ftp = FTP()
            self.ftp.set_debuglevel(2)
            self.ftp.connect(self.host, self.port, timeout=timeout)
            welcome = self.ftp.login(self.username, self.password)
            self.ftp.prot_p()
            
            # 切换到工作目录
            if self.workdir:
                try:
                    self.ftp.cwd(self.workdir)
                    print(f"切换到工作目录: {self.workdir}")
                except Exception as e:
                    print(f"切换到目录失败 {self.workdir}: {e}")
                    # 尝试创建目录
                    try:
                        self.ftp.mkd(self.workdir)
                        self.ftp.cwd(self.workdir)
                        print(f"创建并切换到目录: {self.workdir}")
                    except:
                        print(f"使用根目录")
            
            self.connected = True
            print("✓ 连接成功")
            return True
            
        except Exception as e:
            print(f"✗ 连接失败: {e}")
            self.ftp.quit()
            self.connected = False
            return False
    
    def disconnect(self):
        """断开FTP连接"""
        if self.ftp and self.connected:
            try:
                self.ftp.quit()
                print("✓ 已断开FTP连接")
            except Exception as e:
                print(f"断开连接时出错: {e}")
                try:
                    self.ftp.close()
                except:
                    pass
            finally:
                self.connected = False
                self.ftp = None
    
    def list_files(self, detailed=False):
        """列出目录中的文件"""
        if not self.connected:
            print("未连接到服务器")
            return []
        
        try:
            if detailed:
                # 详细列表
                print("详细文件列表:")
                files = []
                
                def callback(line):
                    files.append(line)
                    print(f"  {line}")
                
                self.ftp.dir(callback=callback)
                return files
            else:
                # 简单列表
                files = self.ftp.nlst()
                print(f"文件列表 ({len(files)} 项):")
                for i, f in enumerate(files, 1):
                    print(f"  {i:2d}. {f}")
                return files
                
        except Exception as e:
            print(f"列出文件失败: {e}")
            return []
    
    def upload_file(self, local_file, remote_file=None):
        """上传文件到FTP服务器"""
        if not self.connected:
            print("未连接到服务器")
            return False
        
        # 检查文件是否存在（MicroPython方式）
        try:
            # 尝试打开文件检查是否存在
            with open(local_file, 'rb') as f:
                pass
        except Exception:
            print(f"本地文件不存在或无法访问: {local_file}")
            return False
        
        if remote_file is None:
            # 从路径中提取文件名
            remote_file = local_file.split('/')[-1]  # MicroPython兼容
        
        try:
            # 获取文件大小
            try:
                with open(local_file, 'rb') as f:
                    f.seek(0, 2)  # 移动到文件末尾
                    file_size = f.tell()
                    f.seek(0)  # 回到文件开头
            except:
                file_size = "未知"
            
            print(f"上传: {local_file} -> {remote_file} ({file_size} 字节)")
            
            # 上传文件
            with open(local_file, 'rb') as f:
                self.ftp.storbinary(f'STOR {remote_file}', f)
            
            print(f"✓ 上传成功: {remote_file}")
            return True
            
        except Exception as e:
            print(f"✗ 上传失败: {e}")
            return False
    
    def download_file(self, remote_file, local_file=None):
        """从FTP服务器下载文件"""
        if not self.connected:
            print("未连接到服务器")
            return False
        
        if local_file is None:
            local_file = remote_file
        
        try:
            print(f"下载: {remote_file} -> {local_file}")
            
            # 尝试获取文件大小
            try:
                size = self.ftp.size(remote_file)
                if size is not None:
                    print(f"文件大小: {size} 字节")
            except:
                pass
            
            # 下载文件
            with open(local_file, 'wb') as f:
                def callback(data):
                    f.write(data)
                
                self.ftp.retrbinary(f'RETR {remote_file}', callback, blocksize=2048)
            
            # 验证下载
            try:
                with open(local_file, 'rb') as f:
                    f.seek(0, 2)
                    downloaded_size = f.tell()
                print(f"✓ 下载成功: {local_file} ({downloaded_size} 字节)")
                return True
            except:
                print("✗ 下载失败: 文件未正确创建")
                return False
                
        except Exception as e:
            print(f"✗ 下载失败: {e}")
            # 清理可能创建的不完整文件
            try:
                os.remove(local_file)
            except:
                pass
            return False
    
    def create_test_file(self, filename, content):
        """创建测试文件（MicroPython兼容）"""
        try:
            with open(filename, 'w') as f:
                if isinstance(content, list):
                    for line in content:
                        f.write(line + '\n')
                else:
                    f.write(content)
            print(f"✓ 创建测试文件: {filename}")
            return True
        except Exception as e:
            print(f"✗ 创建文件失败: {e}")
            return False
    
    def cleanup(self, filenames):
        """清理文件"""
        for filename in filenames:
            try:
                if os.path.exists(filename):  # 注意：MicroPython可能没有os.path.exists
                    os.remove(filename)
                    print(f"清理文件: {filename}")
            except Exception:
                # 尝试直接删除
                try:
                    os.remove(filename)
                except:
                    pass
    
    def test_connection(self):
        """测试连接和基本功能"""
        print("\n" + "="*50)
        print("FTP连接测试")
        print("="*50)
        
        # 1. 连接
        if not self.connect():
            return False
        
        # 2. 显示当前目录
        try:
            pwd = self.ftp.pwd()
            print(f"当前目录: {pwd}")
        except:
            pass
        
        # 3. 列出文件
        print("\n1. 列出服务器文件:")
        self.list_files()
        
        # 4. 创建并上传测试文件
        print("\n2. 上传测试文件:")
        test_content = [
            "FTP测试文件",
            f"服务器: {self.host}:{self.port}",
            f"时间: {time.time()}",
            "这是一个测试文件"
        ]
        
        local_test = "micro_test.txt"
        if self.create_test_file(local_test, test_content):
            if self.upload_file(local_test, "micro_upload_test.txt"):
                print("✓ 测试文件上传成功")
            else:
                print("✗ 测试文件上传失败")
        else:
            print("✗ 无法创建测试文件")
        
        # 5. 再次列出文件
        print("\n3. 更新后的文件列表:")
        self.list_files()
        
        # 6. 下载文件
        print("\n4. 下载测试文件:")
        if self.download_file("micro_upload_test.txt", "micro_downloaded.txt"):
            # 显示下载的内容
            try:
                with open("micro_downloaded.txt", 'r') as f:
                    content = f.read()
                print("下载的文件内容:")
                print("-" * 30)
                print(content)
                print("-" * 30)
            except:
                pass
        
        # 7. 清理测试文件
        print("\n5. 清理测试文件:")
        
        # 从服务器删除
        try:
            self.ftp.delete("micro_upload_test.txt")
            print("✓ 已删除服务器测试文件")
        except:
            print("✗ 删除服务器文件失败")
        
        # 清理本地文件
        self.cleanup([local_test, "micro_downloaded.txt"])
        
        # 8. 最终文件列表
        print("\n6. 最终文件列表:")
        self.list_files()
        
        return True
    
    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.disconnect()


def main():
    """主函数"""
    # FTP服务器配置
    FTP_CONFIG = {
        'host': '112.31.84.164',
        'port': 8311,
        'username': 'test',
        'password': 'GJbMlzZB65',
        'workdir': '/FTP-TEST'
    }
    
    print("MicroPython FTP客户端")
    print(f"服务器: {FTP_CONFIG['host']}:{FTP_CONFIG['port']}")
    print(f"用户: {FTP_CONFIG['username']}")
    print(f"工作目录: {FTP_CONFIG['workdir']}")
    
    # 创建客户端
    client = MicroFTPClient(**FTP_CONFIG)
    
    try:
        # 运行测试
        success = client.test_connection()
        
        if success:
            print("\n" + "="*50)
            print("✓ FTP测试成功完成")
            print("="*50)
        else:
            print("\n" + "="*50)
            print("✗ FTP测试失败")
            print("="*50)
            
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
    except Exception as e:
        print(f"\n发生错误: {e}")
        # 在MicroPython中打印详细错误
        import sys
        sys.print_exception(e)
    finally:
        # 确保断开连接
        client.disconnect()
    
    print("\n程序结束")


# 直接运行的示例
def simple_example():
    """最简单的使用示例"""
    # 创建FTP连接
    ca_content = read_cert_file('/flash/ftp_ca.pem')
        # 2. 配置SSL参数
    ssl_params = {
        "ca": ca_content,          # CA证书内容
        "session_reuse": True,     # 控制通道会话是否复用
    }
    ftp = FTP_TLS(ssl_params=ssl_params)
    #ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect('112.31.84.164', 8311, timeout=30)
    ftp.login('test', 'GJbMlzZB65')
    ftp.prot_p()
    # 切换到工作目录
    try:
        ftp.cwd('/FTP-TEST')
    except:
        print("使用根目录")
    
    # 列出文件
    print("服务器文件:")
    files = ftp.nlst()
    for f in files:
        print(f"  {f}")
    # 上传一个简单文件
    with open('simple.txt', 'w') as f:
        f.write('Hello FTP!\n')
    
    with open('simple.txt', 'rb') as f:
        ftp.storbinary('STOR simple.txt', f)
    print("文件上传成功")
    
    # 断开连接
    ftp.quit()
        


if __name__ == "__main__":
    # 运行主函数
    main()
    
    # 或者运行简单示例
     #simple_example()
