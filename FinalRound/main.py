from input_reader import read_input
import os

if __name__ == '__main__':
    infile = os.path.join('input','me_at_the_zoo.in')
    outfile = infile.split('.')[0] + '.out'
    problem = read_input(infile)
    print problem

    output_file = open(outfile, 'w+')
    output_file.write("ok")
