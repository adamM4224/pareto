from pareto.coverage import coverage
from pareto.transport import transport
from pareto.grid import grid_is_valid
import copy 
import json

def pareto_objective(tree, grid, beta, radius, unit_length, grid_width, grid_height):

    if not grid_is_valid(grid):
        raise Exception('Invalid grid before pareto objective')
    
    cval = coverage(tree, grid, radius, unit_length, grid_width, grid_height)
    
    if not grid_is_valid(grid):
        raise Exception('Invalid grid: Invalid grid after coverage.')
    
    tval = transport(tree, grid)

    if not grid_is_valid(grid):
        raise Exception('Invalid grid: Invalid grid after transport.')
    
    return {
        'beta': beta,
        'coverage': cval, 
        'transport': tval, 
        'value': beta * cval + (1 - beta) * tval
    }