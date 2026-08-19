from .base import RefinementStrategy

class UniformHRefinement(RefinementStrategy):
    def calculate_sizes(self, initial_size, runs, factor) -> list:
        
        sizes = [(initial_size, round(initial_size * factor, 2))]
        
        for i in range(1, runs):
            max_val = sizes[i-1][1]
            min_val = sizes[i-1][1] * factor
            sizes.append((round(max_val, 2), round(min_val, 2)))

        return sizes
