import sys
sys.path.insert(0, 'D:/_Progs/01Center/ODD/实证案例')

# 测试 semaphore_defect - 信号量
from semaphore_defect import Semaphore

sem = Semaphore(2)  # 允许2个并发

print('=== Semaphore测试 ===')
results = []
for i in range(5):
    acquired = sem.acquire(timeout=0.1)
    results.append(acquired)
    print(f'请求{i+1}: {"获取" if acquired else "等待/超时"}')

print(f'\n结果: {results}')
print('预期: [True, True, False, False, False] (如果超时)')
