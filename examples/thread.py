import _thread
import utime
import sys

class ProducerConsumer:
    def __init__(self):
        self.items = []
        self.lock = _thread.allocate_lock()
        self.semaphore = _thread.allocate_semaphore(0)
        self.running = True
        self.producer_count = 0
        self.consumer_count = 0
    
    def producer(self):
        """生产者线程"""
        print("[生产者] 启动")
        
        while self.running:
            self.producer_count += 1
            item = f"商品{self.producer_count}"
            
            with self.lock:
                self.items.append(item)
                print(f"[生产] {item}，库存: {len(self.items)}")
            
            self.semaphore.release()
            
            # 2秒生产一个，但支持中断
            for i in range(40):  # 40 * 50ms = 2秒
                if not self.running:
                    return
                utime.sleep_ms(50)
        
        print("[生产者] 退出")
    
    def consumer(self):
        """消费者线程"""
        print("[消费者] 启动")
        
        while self.running:
            # 等待产品，支持中断
            try:
                if self.semaphore.acquire(500):  # 最多等0.5秒
                    self.consumer_count += 1
                    with self.lock:
                        if self.items:
                            item = self.items.pop(0)
                            print(f"[消费] {item}，剩余: {len(self.items)}")
                else:
                    continue  # 超时，检查退出标志
            except Exception as e:
                if not self.running:
                    break
            
            # 1秒消费一个，但支持中断
            for i in range(20):  # 20 * 50ms = 1秒
                if not self.running:
                    return
                utime.sleep_ms(50)
        
        print("[消费者] 退出")
    
    def status(self):
        """显示状态"""
        with self.lock:
            return f"生产: {self.producer_count}个, 消费: {self.consumer_count}个, 库存: {len(self.items)}"
    
    def stop(self):
        """停止所有线程"""
        print("\n正在停止程序...")
        self.running = False
        
        # 释放信号量让消费者退出
        max_cnt, cur_cnt = self.semaphore.getCnt()
        if cur_cnt == 0:
            self.semaphore.release()
        
        utime.sleep(0.5)
        print(f"最终状态: {self.status()}")
        print("程序已停止")
        sys.exit(0)

def main():
    """主函数"""
    print("=== 生产者消费者演示 ===")
    print("生产者: 2秒/个")
    print("消费者: 1秒/个")
    print("按 Ctrl+C 退出程序\n")
    
    pc = ProducerConsumer()
    
    # 启动线程
    _thread.start_new_thread(pc.producer, ())
    _thread.start_new_thread(pc.consumer, ())
    
    try:
        # 主循环
        counter = 0
        while True:
            utime.sleep(1)
            counter += 1
            
            # 每5秒显示状态
            if counter % 5 == 0:
                print(f"\n[系统状态] {pc.status()}")
    
    except KeyboardInterrupt:
        pc.stop()

if __name__ == "__main__":
    main()