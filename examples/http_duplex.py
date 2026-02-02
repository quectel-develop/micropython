import urequests
import json

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

def main():
    print("=== HTTPS客户端证书请求示例 ===")
    
    # 1. 读取证书文件内容
    print("读取证书文件...")
    ca_content = read_cert_file('/flash/http_ca.pem')
    cert_content = read_cert_file('/flash/http_user.pem')
    key_content = read_cert_file('/flash/http_user_key.pem')
    
    if not all([ca_content, cert_content, key_content]):
        print("❌ 证书文件读取失败，请检查文件路径")
        return
    
    print("✅ 证书文件读取成功")
    
    # 2. 配置SSL参数
    ssl_params = {
        "ca": ca_content,          # CA证书内容
        "cert": cert_content,      # 客户端证书内容  
        "key": key_content         # 客户端私钥内容
    }
    
    # 3. GET请求
    get_url = "https://112.31.84.164:8303/1024.txt"
    print(f"\nGET目标URL: {get_url}")
    
    print("\n正在发起GET请求...")
    try:
        get_response = urequests.get(
            get_url,
            ssl_params=ssl_params,
            timeout=10
        )
        
        print(f"\n✅ GET请求成功!")
        print(f"状态码: {get_response.status_code}")
        
        if get_response.status_code == 200:
            content = get_response.text
            print(f"响应内容 ({len(content)} 字节)")
        else:
            print(f"❌ GET请求失败")
            
        get_response.close()
        
    except Exception as e:
        print(f"\n❌ GET请求异常: {e}")
    
    # 4. POST请求
    post_url = "https://112.31.84.164:8303/upload.php"
    print(f"\nPOST目标URL: {post_url}")
    
    # 准备JSON数据
    post_data = {"url": "https://112.31.84.164:8303/upload.php"}
    
    print("\n正在发起POST请求...")
    try:
        post_response = urequests.post(
            post_url,
            data=json.dumps(post_data),
            headers={'Content-Type': 'application/json'},
            ssl_params=ssl_params,
            timeout=10
        )
        
        print(f"\n✅ POST请求成功!")
        print(f"状态码: {post_response.status_code}")
        print(f"响应: {post_response.text}")
            
        post_response.close()
        
    except Exception as e:
        print(f"\n❌ POST请求异常: {e}")

# 运行主函数
if __name__ == "__main__":
    print("MicroPython HTTPS客户端示例")
    print("=" * 50)
    
    main()
    
    print("\n" + "=" * 50)
    print("脚本执行完成")
