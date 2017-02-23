def read_input(filename):
    with open(filename, 'r') as f:
        grid = []
        line=""
        _, _, min_elt_by_type, max_elts = map(int, line.strip().split())