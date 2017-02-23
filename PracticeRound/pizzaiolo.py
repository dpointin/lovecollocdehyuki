# -*-coding:Latin-1 -*


import math

"""
Google Hash Code pratice round 2017
Naive solution that consists in :
    Taking valid slices from the smallest to the biggest and from 0,0 to n_rows,n_cols
"""
# nouvelle tentative et ça marche !

def get_divisors(n):
    for i in xrange(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            if i != n / i:
                yield (i, n / i)
                yield (n / i, i)
            else:
                yield (i, n / i)


class Pizza:
    def __init__(self, min_elt_by_type, max_elts, grid):
        self.min_elt_by_type = min_elt_by_type
        self.max_elts = max_elts
        self.n_rows = len(grid)
        self.n_cols = len(grid[0])
        self.grid = grid
        self.used_pizza = [[False] * len(grid[0]) for _ in xrange(len(grid))]

    def __str__(self):
        s = "Minimum number of each ingredient = {}\n".format(self.min_elt_by_type)
        s += "Maximum number of ingredients = {}\n".format(self.max_elts)
        s += '\n'.join(row for row in self.grid)
        return s

    def _mark(self, slice_rows, slice_cols, slice_i, slice_j):
        for i in xrange(slice_i, slice_i + slice_rows):
            for j in xrange(slice_j, slice_j + slice_cols):
                self.used_pizza[i][j] = True

    def _is_valid(self, slice_rows, slice_cols, slice_i, slice_j):
        count_t = 0
        count_m = 0
        for i in xrange(slice_i, slice_i + slice_rows):
            for j in xrange(slice_j, slice_j + slice_cols):
                if self.used_pizza[i][j]:
                    return False
                if self.grid[i][j] == 'T':
                    count_t += 1
                elif self.grid[i][j] == 'M':
                    count_m += 1
        if count_t >= self.min_elt_by_type and count_m >= self.min_elt_by_type:
            return True
        else:
            return False

    def _extract_valid_slices(self, slice_rows, slice_cols):
        """
        Get all the valid slices that don't override for a given slice size (rows,cols) starting from 0,0
        """
        for i in xrange(self.n_rows - slice_rows + 1):
            for j in xrange(self.n_cols - slice_cols + 1):
                if self._is_valid(slice_rows, slice_cols, i, j):
                    self._mark(slice_rows, slice_cols, i, j)
                    yield (i, j, i + slice_rows - 1, j + slice_cols - 1)

    def _get_slice_sizes(self):
        for total_slice_size in xrange(self.max_elts, 2 * self.min_elt_by_type - 1, -1):
            for slice_rows, slice_cols in get_divisors(total_slice_size):
                yield slice_rows, slice_cols

    def get_slices(self):
        """
        Start from a slice of size max_elts to the smallest possible and extract the valid slices of
        the corresponding size of the pizza
        """
        # Max slice_size = max_elts, min slice_size = number of elements by type * 2 (nb of different ingredients)
        pizza_slices = []
        for slice_rows, slice_cols in self._get_slice_sizes():
            pizza_slices += self._extract_valid_slices(slice_rows, slice_cols)
        return pizza_slices

    def get_score(self):
        return sum(1 if self.used_pizza[i][j] else 0 for i in xrange(self.n_rows) for j in xrange(self.n_cols))


def read_input(filename):
    with open(filename, 'r') as f:
        grid = []
        min_elt_by_type = 0
        max_elts = 0
        for i, line in enumerate(f.readlines()):
            if i == 0:
                _, _, min_elt_by_type, max_elts = map(int, line.strip().split())
            else:
                grid.append(line.strip())
        return Pizza(min_elt_by_type, max_elts, grid)


if __name__ == '__main__':
    infile = 'big.in'
    outfile = infile.split('.')[0] + '.out'
    pizza = read_input(infile)
    slices = pizza.get_slices()
    output_file = open(outfile, 'w+')
    output_file.write(str(len(slices)) + '\n' + '\n'.join(' '.join(str(i) for i in s) for s in slices))
    print pizza.get_score()
