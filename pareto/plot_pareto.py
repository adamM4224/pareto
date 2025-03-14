

import os
import matplotlib.pyplot as plt
import networkx as nx

def plot_tree(fname, tree, title=None):
    title = title if title else ""


    folder = os.path.dirname(fname)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    pos = nx.spring_layout(tree)
    nx.draw(tree, pos, with_labels=False)
    plt.title(f'{title}')
    plt.savefig(fname)


def plot_pareto(fname, data):
    

    folder = os.path.dirname(fname)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    
    # Extract data for the Pareto plot
    beta = [di['beta'] for di in data]
    values = [di['value'] for di in data]

    x = [vi['coverage'] for vi in values]
    y = [vi['transport'] for vi in values]

    # min max normalize
    min_x, max_x = min(x), max(x)
    min_y, max_y = min(y), max(y)

    norm_x = [(xi - min_x) / (max_x - min_x) for xi in x] if max_x != min_x else x
    norm_y = [(yi - min_y) / (max_y - min_y) for yi in y] if max_y != min_y else y
    trees = [di['tree'] for di in data]

    # Create the Pareto plot and save it
    plt.figure()
    plt.plot(norm_x, norm_y, marker='o')
    plt.xlabel('Transport')
    plt.ylabel('Coverage')
    plt.title('Pareto Plot')

    
    plt.savefig(fname)
    plt.close()

