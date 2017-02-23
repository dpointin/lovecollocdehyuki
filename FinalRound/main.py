from input_reader import read_input

if __name__ == '__main__':
    infile = 'me_at_the_zoo.in'
    outfile = infile.split('.')[0] + '.out'
    problem = read_input(infile)

    output_file = open(outfile, 'w+')
    output_file.write("ok")
