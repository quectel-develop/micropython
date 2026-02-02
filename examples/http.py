import urequests
import json
def main():
    
    get_url = "http://112.31.84.164:8300/1024.txt"
    print(f"\nGET目标URL: {get_url}")
    
    print("\n正在发起GET请求...")
    try:
        get_response = urequests.get(get_url)
        
        print(f"\n✅ GET请求成功!")
        print(f"状态码: {get_response.status_code}")
        
        if get_response.status_code == 200:
            content = get_response.text
            print(f"响应内容 {content}")
        else:
            print(f"❌ GET请求失败")
            
        get_response.close()
        
    except Exception as e:
        print(f"\n❌ GET请求异常: {e}")
    

    post_url = "http://112.31.84.164:8300/upload.php"
    print(f"\nPOST目标URL: {post_url}")
    
    # 准备JSON数据
    post_data = {"url": "https://112.31.84.164:8303/upload.php"}
    
    print("\n正在发起POST请求...")
    try:
        post_response = urequests.post(
            post_url,
            data=json.dumps(post_data),
            headers={'Content-Type': 'application/json'}
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