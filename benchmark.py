from knapsack_benchmark import KnapsackBenchmark
from saport.knapsack.solverfactory import SolverType

problems = [
    # problems to be used in the benchmark
    # you can comment out those you don't want to use
    "ks_4_0", 
    "ks_19_0", 
    "ks_40_0", 
    "ks_50_0",
    "ks_60_0", 
    # "ks_100_0", 
    # "ks_200_0", 
    # "ks_500_0"
]

solvers =[
        # solvers to be benchmarked
        # you can comment out those you don't want to benchmark
        SolverType.DFS,
        SolverType.GREEDY_VALUE,
        SolverType.GREEDY_WEIGHT,
        SolverType.GREEDY_DENSITY,
        SolverType.GREEDY_PORTFOLIO,
        SolverType.DYNAMIC,
        SolverType.BRANCH_AND_BOUND_DFS
    ]

benchmark = KnapsackBenchmark(
    problems,
    solver_types=solvers
)
benchmark.run()
