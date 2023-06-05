from ..solver import Solver
from ..model import Solution, Item
import numpy as np
from typing import List



class DynamicSolver(Solver):
    """
    A naive dynamic programming solver for the knapsack problem.
    """

    def _create_table(self) -> np.ndarray:
        # TODO: fill the table!
        # tip 1. init table using np.zeros function (replace `None``)
        # tip 2. remember to handle timeout (refer to the dfs solver for an example)
        #        - just return the current state of the table
        
        table = np.zeros((self.problem.capacity + 1, len(self.problem.items) + 1), dtype=int)
        
        for i in range(1, len(self.problem.items) + 1):
            for j in range(self.problem.capacity + 1):
                if self.timeout():
                    return table
                
                if self.problem.items[i - 1].weight <= j:
                    table[j, i] = max(table[j, i - 1], table[j - self.problem.items[i - 1].weight, i - 1] + self.problem.items[i - 1].value)
                else:
                    table[j, i] = table[j, i - 1]
                
        return table

    def _extract_solution(self, table: np.ndarray) -> Solution:
        used_items: List[Item] = []
        optimal = table[-1, -1] > 0

        # TODO: fill in the `used_items` list using info from the table!
        i = len(self.problem.items)
        j = self.problem.capacity
        
        while i > 0 and j > 0:
            if self.timeout():
                return Solution.from_items(used_items, optimal)

            if table[j, i] != table[j, i - 1]:
                used_items.append(self.problem.items[i - 1])
                j -= self.problem.items[i - 1].weight
            i -= 1
            
        return Solution.from_items(used_items, optimal)

    def solve(self) -> Solution:
        self.interrupted = False
        self.start_timer()

        table = self._create_table()
        solution = self._extract_solution(table) if table is not None else Solution.empty()

        self.stop_timer()
        return solution
