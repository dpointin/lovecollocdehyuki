from input_reader import read_input
import os

if __name__ == '__main__':
    for filename in ["kittens","me_at_the_zoo","trending_today","videos_worth_spreading"] :
        print filename
        infile = os.path.join('input', filename)+'.in'
        outfile = os.path.join('naive', filename)+'.out'
        problem = read_input(infile)
        problem.solution_naive()
        output_file = open(outfile, 'w+')
        output_file.write(problem.output_sol())
        output_file.close()
