import numpy as np
import sys
from pareto.Pareto import Pareto
from pareto.grid import get_grid
from pareto.plot_pareto import plot_pareto, plot_tree
import json
from get_data import get_data


def get_experiment_settings(json_settings_file="./settings/defaults.json"):
    """"
    Global settings for experiment. It is actually just returning 
    what is in the json file. Removing grid transform function from 
    here so the settings can be json. Update the grid on the pareto.set_grid()


    Parameters: 
        json_settings_file: {unit_length: float, radius: float}
        * see settings/default.json for example

    Returns

        transform_func: function - to transform the default grid (uniform nutrients)
            params: grid
            returns: grid (see src/grid.py for what makes a valid grid)
    """
    s = None
    with open(json_settings_file) as f:
        s =  json.load(f)
    return {
        'unit_length': s['unit_length'],
        'radius': s['radius'],
        'key': s['key'] if 'key' in s else ''
    }

def build_pareto(data_instance, settings):
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
    # settings = get_experiment_settings()

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

        # update grid here
        # pareto.set_grid(grid)

        tree, grid, value = pareto.build()
        optimal_structures.append({
            'beta': beta, 
            'tree': tree, 
            'grid': grid,
            'value': value
        })

    return optimal_structures


def main():
    settings_file = sys.argv[1] if len(sys.argv) > 1 else None 
    settings_file = settings_file or './settings/default.json' 
    settings = get_experiment_settings(settings_file)

    data = get_data()
    for i, di in enumerate(data):
        # update the name to include the experimental details
        name = di['name']
        name = f"{name}-{settings['key']}"
        print(f'running: {name}')
        di['name'] = name
        values = build_pareto(di, settings)
        plot_pareto(f'./figures/{name}.pcurve.png', values)

        for vi in values:
            tree = vi['tree']
            beta = vi['beta']
            tname = f"./tree_pngs/{name}_{beta:.2}.tree.png"
            plot_tree(tname, tree, title=f"{name} - {beta:.2}")
        




if __name__ == '__main__':
    main()