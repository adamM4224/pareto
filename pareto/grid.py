"""
Grid:
    grid = [[{nutrient: boolean, available: boolean}, ....]]

    Grids used throughout the program must adhere to the above structure
    Each cell of the grid is an object with keys:
        nutrient: whether a nutrient is at the location
        available: if a nutrient is present, has it been used.
"""

def get_grid(width, height, unit_length=1, transform_func=None):
    """
    Returns a grid of points with the given dimensions.
    The width and height are broken into i-j indices by the 
    unit length.

    Params:
        width: float 
        height: float 
        unit_length: float - distribute 
        transform_func: function - takes the grid as parameter and 
                        returns a valid grid. The grid is uniform 
                        with nutrients so that can be adjusted by 
                        user here.
    """
    transform_func = transform_func if transform_func else lambda x: x
    rows = int(height / unit_length)
    cols = int(width / unit_length)
    grid = [[{
        'nutrient': True, 
        'available': True,
        'aquired_by_node_id': None
    } for j in range(cols)] for i in range(rows)]
    return transform_func(grid) 

def grid_is_valid(grid):
    """
    Takes a grid and checks and ensures it is valid.
    """
    valid = type(grid) == list and len(grid) and type(grid[0]) == list 
    if not valid:
        return False
    
    for row in grid:
        for cell in row:
            valid = type(cell) == dict 
            valid = valid and 'nutrient' in cell 
            valid = valid and 'available' in cell
    return valid

def grids_are_equal(grid1, grid2):
    """"
    Debugging function
    """
    f = lambda x1, x2: x1['nutrient'] == x2['nutrient'] and x1['available'] == x2['available']
    
    equal = len(grid1) == len(grid2) and len(grid1[0]) == len(grid2[0])
    for i in range(len(grid1)):
        for j in range(len(grid1[0])):
            equal = equal and f(grid1[i][j], grid2[i][j])
    return equal

def grid_meta(grid):
    """"
    Debugging function
    """
    if not grid_is_valid(grid):
        raise ValueError("Grid id not valid: Can't obtain metadata")    

    flat_grid = [item for sublist in grid for item in sublist]
    
    n_rows = len(grid)
    n_cols = len(grid[0])
    n_cells = n_rows * n_cols
    total_nutrients = sum([1 for gi in flat_grid if 'nutrient' in gi and gi['nutrient']])
    nutrients_acquired = sum([1 for gi in flat_grid if 'available' in gi and not gi['available']])

    return {
        'n_rows': n_rows,
        'n_cols': n_cols,
        'n_cells': n_cells,
        'total_nutrients': total_nutrients,
        'nutrients_acquired': nutrients_acquired
    }

def grid_ids(grid):
    """"
    debugging function
    """
    if not grid_is_valid(grid):
        raise ValueError("Grid id not valid: Can't obtain grid ids")        
    
    ids = []
    for row in grid:
        for cell in row:
            if 'acquired_by_node_id' in cell:
                ids.append(cell['acquired_by_node_id']) 

    return ids