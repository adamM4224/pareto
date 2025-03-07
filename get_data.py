
def get_data():
    return [
        {'name': 'A', 'length': 100, 'n_segments': 20},
        {'name': 'B', 'length': 200, 'n_segments': 30},
        {'name': 'C', 'length': 250, 'n_segments': 25}
    ]

# replace this when ready
def get_real_data(segment_length=10):
    data = []
    tm = [str, int, float, float]
    with open('./data/data.csv') as f:
        data = [line.strip().replace('\n', '').split(',') for i, line in enumerate(f) if i]
        data = [[fi(di) for di, fi in zip(row, tm)] for row in data]
    
    return [{
        'name': f"{row[0]}-{row[1]}",
        "length": row[2],
        "n_segments": segment_length if segment_length else row[3]
    } for row in data]
    

