# gnss_thread.py - 带退出标志的版本

import quectel
import time
import _thread

# 全局变量
gnss = None
running = True  # 添加退出标志

def gnss_loop():
    global gnss, running
    
    gnss = quectel.GNSS()
    if not gnss.start():
        print("GNSS启动失败!")
        return
    
    print("开始循环打印定位信息...")
    
    while running:  # 使用退出标志
        try:
            loc = gnss.get_location()
            if loc:
                print(f"[{time.time():.0f}] 纬度:{loc['latitude']:.6f}, 经度:{loc['longitude']:.6f}")
            else:
                print(f"[{time.time():.0f}] 定位中...")
            time.sleep(1)
        except Exception as e:
            print(f"错误: {e}")
            break
    
    # 退出循环后清理
    if gnss:
        gnss.stop()
        print("GNSS线程已退出")

# 启动线程
_thread.stack_size(4096)
_thread.start_new_thread(gnss_loop, ())
print("GNSS线程已启动，按Ctrl+C停止")

# 主线程
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n正在停止...")
    running = False  # 通知线程退出
    time.sleep(2)    # 等待线程退出
    print("程序退出")