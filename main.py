import numpy as np
from pareto.Pareto import Pareto
from pareto.grid import get_grid
from pareto.plot_pareto import plot_pareto
import json
from get_data import get_data


def get_experiment_settings():
    """"
    Global settings for experiment
    Returns
        unit_length: float - the unit length of a grid cell
        radius: float - radius to look around point (xi, yi) for nutrients
        transform_func: function - to transform the default grid (uniform nutrients)
            params: grid
            returns: grid (see src/grid.py for what makes a valid grid)
    """
    return {
        'unit_length': 1,
        'radius': 10, 
        'transorm_func': lambda x: x
    }

def build_pareto(data_instance):
    """
    Build the pareto curve. Computes coverage, transport objectives over a
    range of beta values.

    Parameters:
        data_instance: dict
            name: string,
            n_segments: int
            length: float
    
    Returns:
        [{beta, tree, grid, value}, ....]
        - value = {coverage, transport, beta}
    """
    di = data_instance 
    name = di['name']
    length = di['length']
    n_segments = di['n_segments']
    segment_length = length / n_segments 
    settings = get_experiment_settings()

    optimal_structures = []

    for beta in np.arange(0, 1, .2):
        beta = float(beta)
        
        if not beta: 
            continue
        
        pareto = Pareto(
            name, 
            beta, 
            segment_length,
            n_segments,
            settings['radius'],
            unit_length=settings["unit_length"]
        )

        tree, grid, value = pareto.build()
        optimal_structures.append({
            'beta': beta, 
            'tree': tree, 
            'grid': grid,
            'value': value
        })

    return optimal_structures


def main():

    data = get_data()
    for i, di in enumerate(data):
        values = build_pareto(di)
        plot_pareto(f'test1{i}', values)



if __name__ == '__main__':
    main()