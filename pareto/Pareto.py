from pareto.grid import get_grid, grid_is_valid
import numpy as np
import networkx as nx
import copy
from pareto.pareto_objective import pareto_objective
from uuid import uuid4
from pareto.log import getLogger 



class Pareto:
    """
    Given a value of beta and other params, build the optimal pareto structures
    
    name: string - unique name to data
    beta: float - 0 - 1
    segment_length: float - length of segment to add per iteration
    n_segments: int number of segments to add to the tree
    radius: given a node in the tree, a distance to look around for nutrients
    unit_length: length of a grid cell. 

    In addition to setting parameters the function also creates 
    grid: a valid grid described by grid.py 
    """
    def __init__(
        self,
        name, 
        beta,
        segment_length, 
        n_segments,
        radius,
        unit_length=1        
    ):
        self.name = name
        self.segment_length = segment_length
        self.n_segments = n_segments
        self.radius = radius
        self.unit_length = unit_length
        self.beta = beta
        self.grid_width = 2 * n_segments  * segment_length
        self.grid_height = self.grid_width
        self.logging = getLogger(f'./logs/{self.name}.pareto.log')
        self.log_params()

        self.grid = get_grid(self.grid_width, self.grid_height, unit_length)
        if not grid_is_valid(self.grid):
            raise Exception('Invalid grid: On initialization')
        for row in self.grid:
            for cell in row:
                cell['aquired_by_segment_id'] = None

        self.best_grid = None
        self.best_tree = None

    def set_grid(self, grid):
        """
        Default grid is uniform nutrients, but that can be replaced 
        before building with this call.
        """
        self.grid = grid
        return self
    
    def get_grid(self):
        return copy.deepcopy(self.grid)

    
    def set_radius(self, radius):
        self.radius = radius
        return self
    
    def set_unit_length(self, unit_length):
        self.unit_length = unit_length
        return self
    
    def log_params(self):
        def l(var): 
            val = getattr(self,  var)
            self.logging.info(f"{var}: {val}")
        l("name") 
        l("beta")
        l("segment_length") 
        l("n_segments")
        l("radius")
        l("unit_length")
        self.logging.info("---------------")
        return self
        
    def build_optimal_structure(self):
        """"
        Runs the algorithm. Builds the tree, calls the objective functions,
        and finds the best structure at each iteration. 

        Returns:
            tree - optimal tree
            grid - the final grid
            value - final values
                - [{beta, coverage, transport}, ....]
        """
        beta = self.beta
        segment_length = self.segment_length
        n_segments = self.n_segments
        grid = self.get_grid()
        radius = self.radius
        grid_width = self.grid_width 
        grid_height = self.grid_height
        unit_length = self.unit_length

        tree = nx.DiGraph()
        root = (0, 0)
        
        # build the tree - a unique node id is required
        tree.add_node(root, id="#root")
        prev = root
        best_pval = 0 # pareto value {beta, coverage, transport}
        
        for i in range(n_segments):
            # 1) get previous node
            # 2) build trees
            # 3) compute objective for each tree
            # 4) find best, set variables 

            # 1
            prev_x = prev[0]
            prev_y = prev[1] 

            # 2 - build trees
            left_tree = copy.deepcopy(tree)
            left_coord = (prev_x - segment_length, prev_y)
            left_tree.add_node(left_coord, id=str(uuid4()))
            left_tree.add_edge(prev, left_coord, id=str(uuid4()))
            
            right_tree = copy.deepcopy(tree)
            right_coord = (prev_x + segment_length, prev_y)
            right_tree.add_node(right_coord, id=str(uuid4()))
            right_tree.add_edge(prev, right_coord, id=str(uuid4()))

            bottom_tree = copy.deepcopy(tree)
            bottom_coord = (prev_x, prev_y + segment_length)
            bottom_tree.add_node(bottom_coord, id=str(uuid4()))
            bottom_tree.add_edge(prev, bottom_coord, id=str(uuid4()))

            # 3 - arrange data and compute objective
            coords = [
                left_coord, 
                right_coord, 
                bottom_coord
            ]
            trees = [
                left_tree, 
                right_tree, 
                bottom_tree
            ] 
            grids = [
                self.get_grid(),
                self.get_grid(),
                self.get_grid()
            ]

            # Boom
            pvals = [
                pareto_objective(trees[0], grids[0], beta, radius, unit_length, grid_width, grid_height),
                pareto_objective(trees[1], grids[1], beta, radius, unit_length, grid_width, grid_height),
                pareto_objective(trees[2], grids[2], beta, radius, unit_length, grid_width, grid_height)
            ]
            
            # find the index of best pareto value. Use index to get all values of interest.
            vals = [pi['value'] for pi in pvals]
            best_value = max(vals)
            best_index = vals.index(best_value)
            
            tree = trees[best_index]
            best_pval = pvals[best_index]
            prev = coords[best_index]
            grid = grids[best_index]
            
            if not grid_is_valid(grid):
                self.logging.error(f"Invalid grid: {grid}")
                raise Exception('Cannot set grid. Invalid')
            
            self.logging.info(f"Loop for i in n_segments: i={i}")
            self.logging.info(f"best_index: {best_index}")
            self.logging.info(f"len(tree): {tree.number_of_nodes()}")
            self.logging.info(f"coord({prev[0]}, {prev[1]})")
            self.logging.info(f"coverage: {best_pval['coverage']}")
            self.logging.info(f"transport: {best_pval['transport']}")
            self.logging.info(f"")

        return tree, self.grid, best_pval

    
    def build(self):
        if not self.grid:
            raise Exception('Grid not set. Please set the grid before running. LINK TO GRID FILE')
        if not grid_is_valid(self.grid):
            
            raise Exception('Invalid grid: Muse set valid grid before building. Lin 13-')
        return self.build_optimal_structure()