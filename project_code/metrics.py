import time
import os
import hyperparameters
import matplotlib.pyplot as plt

class run_metrics():

    def __init__(self, start, end) -> None:
        self.START_NODE         = start
        self.END_NODE           = end
        self.PROJECT_ROOT_DIR   = hyperparameters.proj_root
        self.RUNS_PER_ROUTE     = hyperparameters.num_runs
        self.POPSIZE            = hyperparameters.population_size
        self.XOVER              = hyperparameters.crossover_strategy
        self.GEN_LIMIT          = hyperparameters.max_generations
        self.NUM_ISLANDS        = hyperparameters.num_islands
        self.MIGRATION_INTERVAL = hyperparameters.migration_interval
        self.NUM_MIGRANTS       = hyperparameters.num_migrants
        self.CURR_TIME = time.strftime("%Y%m%d-%H%M%S")
        self.FOLDER = f'{self.CURR_TIME}_{self.START_NODE}_to_{self.END_NODE}'
        self.SAVE_DIR = os.path.join(self.PROJECT_ROOT_DIR, 'run_metrics', self.FOLDER)
        if not os.path.exists(self.SAVE_DIR):
            os.makedirs(self.SAVE_DIR)
        
    def save_hyperparameters(self):
        with open(f'{self.SAVE_DIR}/hyperparameters.txt', 'w') as f:
            f.write(f'Start node              = {self.START_NODE}\n')
            f.write(f'End node                = {self.END_NODE}\n')
            f.write(f'Number of runs          = {self.RUNS_PER_ROUTE}\n')
            f.write(f'Population size         = {self.POPSIZE}\n')
            f.write(f'Crossover strategy      = {self.XOVER}\n')
            f.write(f'Max generations per run = {self.GEN_LIMIT}\n')
            f.write(f'Number of islands       = {self.NUM_ISLANDS}\n')
            f.write(f'Migration interval      = {self.MIGRATION_INTERVAL}\n')
            f.write(f'Number of migrants      = {self.NUM_MIGRANTS}\n')

    def create_results_plot(self, runs_best_result, runs_average_result):
        plt.figure()
        plt.plot(range(len(runs_best_result)), runs_best_result, label="Best Result Per Run")
        plt.plot(range(len(runs_average_result)), runs_average_result, label="Average Result Per Run")
        plt.legend()
        plt.savefig(f'{self.SAVE_DIR}/avg_and_best_results_over_runs.png', bbox_inches='tight')

    
    def create_execution_times_plot(self, execution_times, average_execution_time):
        plt.figure()
        plt.plot(range(len(execution_times)), execution_times, label='Execution Times Per Run')
        plt.plot(range(len(average_execution_time)), average_execution_time, label='Average Execution Time')
        plt.legend()
        plt.savefig(f'{self.SAVE_DIR}/execution_times.png', bbox_inches='tight')
    
    def create_fitness_plot(self, runs_generational_average_fitness):
        plt.figure()
        for generational_average_fitness in runs_generational_average_fitness:
            plt.plot(range(len(generational_average_fitness)), generational_average_fitness)
        plt.savefig(f'{self.SAVE_DIR}/avg_fitness_over_generations.png', bbox_inches='tight')