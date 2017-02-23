from input_reader import read_input



if __name__ == '__main__':
    infile = 'big.in'
    outfile = infile.split('.')[0] + '.out'
    read_input(infile)
    output_file = open(outfile, 'w+')
    output_file.write("ok")