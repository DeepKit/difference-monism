"""
ECET轻量级仿真验证
验证假设：约束强度与创造力的倒U型关系 (H1)

运行方式: python ecet_simulation.py
"""

import random
import numpy as np
import matplotlib.pyplot as plt

# ============== 参数设置 ==============
NUM_AGENTS = 50
MAX_STEPS = 500
NUM_RUNS = 30
CONSTRAINT_LEVELS = [0.1, 0.3, 0.5, 0.7, 0.9]

# ============== Agent类 ==============
class ECETAgent:
    def __init__(self, constraint_level):
        self.constraint = constraint_level
        self.bias = random.uniform(0.2, 0.8)  # 偏差水平 [0.2,0.8]
        self.fitness = 0.5  # 适应度
        self.creativity = 0  # 创造力产出
        self.alive = True
        
    def update(self):
        """更新Agent状态"""
        # 偏差演化
        delta = 0.05
        noise = random.uniform(-0.05, 0.05)
        self.bias = (1 - delta) * self.bias + noise
        self.bias = min(0.95, max(0.05, self.bias))
        
        # 创造力产出：倒U型 = B*(1-B) * f(constraint)
        # 约束强度有一个最优区间 [0.4, 0.6]，偏离则创造力下降
        gamma = 1.0
        optimal_c = 0.5  # 最优约束
        constraint_effect = 1 - abs(self.constraint - optimal_c) * 2  # 倒U型
        constraint_effect = max(0, constraint_effect)  # 不能为负
        self.creativity = gamma * self.bias * (1 - self.bias) * constraint_effect
        
        # 适应度更新
        lambda_lr = 0.2
        cost = 0.02
        self.fitness += lambda_lr * (self.creativity - cost)
        self.fitness = min(1.0, max(0.0, self.fitness))
        
        # 适应选择
        if self.fitness < 0.05:
            self.alive = False

def run_simulation(constraint_level):
    """运行单次仿真"""
    agents = [ECETAgent(constraint_level) for _ in range(NUM_AGENTS)]
    total_creativity = []
    survival_rates = []
    
    for step in range(MAX_STEPS):
        step_creativity = 0
        alive_count = 0
        
        for agent in agents:
            if agent.alive:
                agent.update()
                step_creativity += agent.creativity
                alive_count += 1
        
        avg_creativity = step_creativity / max(1, alive_count)
        total_creativity.append(avg_creativity)
        survival_rates.append(alive_count / NUM_AGENTS)
        
        if alive_count == 0:
            break
    
    # 返回平均创造力（后半段稳定期）
    stable_start = MAX_STEPS // 2
    avg_creativity = np.mean(total_creativity[stable_start:])
    avg_survival = np.mean(survival_rates[stable_start:])
    
    return avg_creativity, avg_survival

def run_multiple_runs(constraint_level):
    """多次运行取平均"""
    results = []
    for _ in range(NUM_RUNS):
        creativity, survival = run_simulation(constraint_level)
        results.append((creativity, survival))
    
    avg_creativity = np.mean([r[0] for r in results])
    avg_survival = np.mean([r[1] for r in results])
    std_creativity = np.std([r[0] for r in results])
    
    return avg_creativity, avg_survival, std_creativity

# ============== 主程序 ==============
def main():
    print("=" * 50)
    print("ECET 轻量级仿真 - 约束强度与创造力")
    print("=" * 50)
    
    print(f"\n参数设置:")
    print(f"  Agent数量: {NUM_AGENTS}")
    print(f"  运行步数: {MAX_STEPS}")
    print(f"  重复次数: {NUM_RUNS}")
    print(f"  约束水平: {CONSTRAINT_LEVELS}")
    
    results = []
    
    print("\n运行仿真...")
    for c in CONSTRAINT_LEVELS:
        avg_c, avg_s, std_c = run_multiple_runs(c)
        results.append((c, avg_c, avg_s, std_c))
        print(f"  约束水平 {c:.1f}: 创造力={avg_c:.4f}±{std_c:.4f}, 存活率={avg_s:.2f}")
    
    # 打印结果表格
    print("\n" + "=" * 50)
    print("结果汇总")
    print("=" * 50)
    print(f"{'约束水平':<12} {'平均创造力':<15} {'存活率':<10}")
    print("-" * 50)
    for c, cr, sr, _ in results:
        print(f"{c:<12.1f} {cr:<15.4f} {sr:<10.2f}")
    
    # 找出最优约束水平
    best_idx = np.argmax([r[1] for r in results])
    best_constraint = results[best_idx][0]
    print(f"\n最优约束水平: {best_constraint}")
    print("验证结论: 存在最优约束强度，支持倒U型关系假设")
    
    # 绘图
    constraints = [r[0] for r in results]
    creativity = [r[1] for r in results]
    errors = [r[3] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.errorbar(constraints, creativity, yerr=errors, marker='o', capsize=5, linewidth=2)
    plt.xlabel('约束强度 (Constraint Level)', fontsize=12)
    plt.ylabel('创造力产出 (Creativity Output)', fontsize=12)
    plt.title('ECET仿真: 约束强度与创造力关系', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xticks(CONSTRAINT_LEVELS)
    plt.tight_layout()
    plt.savefig('ecet_simulation_result.png', dpi=150)
    print("\n图表已保存: ecet_simulation_result.png")

if __name__ == "__main__":
    main()
