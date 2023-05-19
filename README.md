# Lab 06 - Knapsack Problem

The goal of this is lab is to implement various solvers for the knapsack problem.
One has to: fill missing code in: 
  * [ ] `saport.knapsack.solvers.greedy`
  * [ ] `saport.knapsack.solvers.dynamic`
  * [ ] `saport.knapsack.solvers.bnb_dfs`
  
The `saport.knaspack.solvers.dfs` is already implemented, you may use the `benchmarks.py` to compare the performance of the implemented solvers. 

## SAPORT

SAPORT = Student's Attempt to Produce an Operation Research Toolkit

The project depends on the fairly recent numpy distribution and Python interpreter (version >= `3.9` is recommended). All depedendencies are listed in `requirements.txt`. One can install them with simple `pip install -r requirements.txt`, but using a virtual environment (e.g. virtualenv) is encouraged ([official tutorial](https://docs.python.org/3/tutorial/venv.html)). 

## Unit Tests

The `tests` folder contains unit tests written using `pytest`. 
Run it via `pytest`/`pycharm`/`vscode`.

## Benchmark

The `knapsack_problems` folder contains some input instances. You may benchmark your solvers by running: `python benchmark.py`.
This script is **not** used in the grading process. You may want to edit the `benchmark.py` to enable/disable solvers or problems.

## GitLab Setup 

* [ ] Make sure, you have a **private** group 
  * [how to create a group](https://docs.gitlab.com/ee/user/group/#create-a-group)
* [ ] Add @bobot-is-a-bot as the new group member (role: **maintainer**)
  * [how to add a group member](https://docs.gitlab.com/ee/user/group/#add-users-to-a-group)
* [ ] Fork this project into your new **private** group
  * [how to create a fork](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html#creating-a-fork)

## How To Submit Solutions

* [ ] Clone repository: git clone:
    ```bash 
    git clone <repository url>
    ```
* [ ] Solve the exercises 
    * remember to change only files with `#TODO` comments
* [ ] Commit your changes
    ```bash
    git add <path to the changed files>
    git commit -m <commit message>
    ```
* [ ] Push changes to the gitlab master branch
    ```bash
    git push -u origin master
    ```

The rest will be taken care of automatically. You can check the `GRADE.md` file for your grade / test results. Be aware that it may take some time (up to one hour) till this file appears / gets updated. 

## Repository Guide

```bash
.
├── README.md     # this README
├── conftest.py   # this file makes sure pytest works correctly :P
├── knapsack_problems # this folder contains some example inputs used in tests
│   ├── ...
│   └── ks_4_0 # an input example
├── benchmark.py # script to run a solver benchmark
├── knapsack_benchmark.py # benchmark implementation
├── requirements.txt   # python libraries required by the problem
├── saport            
│   ├── knapsack  # folder with knapsack related code
│       ├── model.py   # straightforward representation of the problem and its solution
│       ├── solver.py  # an abstract class (interface) for the knapsack solver
│       ├── solverfactory.py # class creating solvers based on their type (used in bechmark)
│       └── solvers # folder with knapsack solvers
│           ├── dfs.py # basic DFS solver for knapsack problems
│           ├── greedy.py # TODO: greedy solver for knapsack problems
│           ├── dynamic.py # TODO: naive dynamic solver 
│           └── bnb_dfs.py # TODO: DFS solver using a Branch and Bound strategy with linear relaxation
└── tests 
```
