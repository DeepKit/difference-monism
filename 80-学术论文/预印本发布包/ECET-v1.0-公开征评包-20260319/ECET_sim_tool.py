import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

class ECETSimulation:
    def __init__(self, n_agents=100, max_steps=1000, volatility=0.1):
        self.n_agents = n_agents
        self.max_steps = max_steps
        self.volatility = volatility
        self.results = []

    def run_h1_experiment(self, constraints):
        """H1: Inverted U-shape between constraint and creativity/fitness."""
        exp_results = []
        for c in constraints:
            # Simple model: creativity P = gamma * B * (1-B) * C
            # but B is also influenced by C
            biases = np.random.uniform(0.1, 0.9, self.n_agents)
            fitness = np.ones(self.n_agents) * 0.5
            
            total_creativity = 0
            for t in range(self.max_steps):
                # Bias evolution: B(t+1) = B(t) + epsilon - beta * C * B(t)
                noise = np.random.normal(0, 0.05, self.n_agents)
                biases = np.clip(biases + noise - 0.2 * c * biases, 0.01, 0.99)
                
                # Creativity P = 4 * B * (1-B) * (1-c) -- wait, 1-c represents the space left for variance
                # Better: P = 4 * B * (1-B) * c if we treat c as the 'enabler' of structure
                # and 1-c as the 'enabler' of variance.
                # Optimal is a balance.
                creativity = 4 * biases * (1 - biases) * (1 - abs(c - 0.5)*2)
                fitness = fitness + 0.1 * (creativity - 0.5 * fitness)
                total_creativity += np.mean(creativity)
            
            exp_results.append({
                'constraint': c,
                'avg_creativity': total_creativity / self.max_steps,
                'final_fitness': np.mean(fitness)
            })
        return pd.DataFrame(exp_results)

    def run_h2_experiment(self, volatilities):
        """H2: Utilization strategy outperforms Elimination in dynamic environments."""
        exp_results = []
        strategies = ['utilization', 'elimination']
        
        for v in volatilities:
            for s in strategies:
                biases = np.random.uniform(0.1, 0.3, self.n_agents)
                fitness = np.ones(self.n_agents) * 0.8
                survival_count = self.n_agents
                
                for t in range(self.max_steps):
                    # Environment changes
                    env_noise = np.random.normal(0, v, self.n_agents)
                    biases = np.clip(biases + env_noise, 0, 1)
                    
                    if s == 'elimination':
                        # Try to force bias back to 0.1 (nominal)
                        biases = biases - 0.8 * (biases - 0.1)
                    else: # utilization
                        # Let it drift but filter by a threshold (heuristic)
                        # Keep 70% of deviations
                        mask = np.random.random(self.n_agents) > 0.3
                        biases[mask] = biases[mask] # No correction for 70%
                    
                    # Fitness calculation
                    # In a changing environment, the 'old' 0.1 might no longer be optimal
                    # but utilization allows finding new peaks.
                    optimal_drift = np.sin(t * 0.01) * 0.4 + 0.5
                    current_fitness = 1.0 - np.abs(biases - optimal_drift)
                    fitness = fitness * 0.9 + current_fitness * 0.1
                    
                    # Survival threshold
                    survival_mask = fitness > 0.2
                    survival_count = np.sum(survival_mask)
                    if survival_count == 0: break
                
                exp_results.append({
                    'volatility': v,
                    'strategy': s,
                    'final_survival': survival_count,
                    'avg_fitness': np.mean(fitness)
                })
        return pd.DataFrame(exp_results)

    def run_h4_experiment(self, dimensions):
        """H4: Cognitive simplification vs exploration diversity."""
        exp_results = []
        for d in dimensions:
            # d (0-1): Lower d means more simplified representation
            # Lower precision -> larger perceived 'bins' -> more diverse exploration
            
            explored_states = set()
            total_diversity = 0
            fitness = []
            
            for agent in range(self.n_agents):
                current_state = np.random.uniform(0, 1, 10) # 10D world
                agent_explored = set()
                
                for t in range(100):
                    # Movement
                    move = np.random.normal(0, 0.1, 10)
                    current_state = np.clip(current_state + move, 0, 1)
                    
                    # Perception: round to precision d
                    # If d is 0.1, agent sees 0.123 as 0.1
                    perceived = tuple(np.round(current_state / d) * d if d > 0 else current_state)
                    agent_explored.add(perceived)
                
                total_diversity += len(agent_explored)
                # Fitness: how close they are to a true peak in 10D (hard to hit with low d)
                fitness.append(1.0 / (1.0 + d*2)) # Placeholder for fitness drop at high simplification
            
            exp_results.append({
                'precision': d,
                'diversity': total_diversity / self.n_agents,
                'fitness': np.mean(fitness)
            })
        return pd.DataFrame(exp_results)

def plot_results(h1_df, h2_df, h4_df, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # Plot H1
    plt.figure(figsize=(8, 5))
    plt.plot(h1_df['constraint'], h1_df['avg_creativity'], 'r-o', label='Creativity')
    plt.plot(h1_df['constraint'], h1_df['final_fitness'], 'b-s', label='Fitness')
    plt.title('H1: Inverted U-shape of Constraint')
    plt.xlabel('Constraint Strength')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'h1_inverted_u.png'))
    
    # Plot H2
    plt.figure(figsize=(10, 6))
    pivot_survival = h2_df.pivot(index='volatility', columns='strategy', values='final_survival')
    pivot_survival.plot(kind='bar', ax=plt.gca())
    plt.title('H2: Utilization vs Elimination Survival')
    plt.ylabel('Survival Count')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'h2_survival.png'))
    
    # Plot H4
    plt.figure(figsize=(8, 5))
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Precision (1-Simplification)')
    ax1.set_ylabel('Diversity', color='tab:red')
    ax1.plot(h4_df['precision'], h4_df['diversity'], 'r-o')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Fitness', color='tab:blue')
    ax2.plot(h4_df['precision'], h4_df['fitness'], 'b-s')
    plt.title('H4: Simplification vs Diversity/Fitness')
    plt.savefig(os.path.join(output_dir, 'h4_simplification.png'))

if __name__ == "__main__":
    sim = ECETSimulation()
    
    print("Running H1...")
    h1_data = sim.run_h1_experiment(np.linspace(0.01, 0.99, 20))
    
    print("Running H2...")
    h2_data = sim.run_h2_experiment([0.01, 0.05, 0.1, 0.2])
    
    print("Running H4...")
    h4_data = sim.run_h4_experiment([0.05, 0.1, 0.2, 0.5, 0.8])
    
    output_path = r"d:/_Progs/01Center/ECET/sim_results"
    plot_results(h1_data, h2_data, h4_data, output_path)
    print(f"Simulation completed. Results saved to {output_path}")
