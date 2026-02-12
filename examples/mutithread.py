import _thread

import utime


# 设置日志输出级别

a = 0
state = 1
state1 = 1
# 创建一个lock的实例
lock = _thread.allocate_lock()

def th_func(delay, id):
    global a
    global state,state1
    while True:
    	lock.acquire()  # 获取锁
    	if a >= 10:
    		print('thread %d exit' % id)
    		lock.release()  # 释放锁
    		if id == 1:
    			state = 0
    		else:
    			state1 = 0
    		break
    	a += 1
    	print('[thread %d] a is %d' % (id, a))
    	lock.release()  # 释放锁
    	utime.sleep(delay)

test = False
def th_func1():
    global test
    while True:
        if test is True:
            break
    	print('thread th_func1 is running')
    	utime.sleep(1)

if __name__ == '__main__':
    for i in range(2):
    	_thread.start_new_thread(th_func, (i + 1, i))   # 创建一个线程，当函数无参时传入空的元组

    thread_id = _thread.start_new_thread(th_func1, ())   # 创建一个线程，当函数无参时传入空的元组

    while state or state1:
    	utime.sleep(1)
    	pass

    test = True
    _thread.delete_lock(lock)   # 删除锁
    print('thread th_func1 is stopped')
