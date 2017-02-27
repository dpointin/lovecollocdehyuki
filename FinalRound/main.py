from input_reader import read_input
import os
import logging
import sys

if __name__== '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    for filename in ["me_at_the_zoo","trending_today","videos_worth_spreading","kittens"] :
        logging.info('*'*10+' '+filename+' '+'*'*10)
        infile = os.path.join('input', filename)+'.in'
        outfile = os.path.join('over_video_size', filename)+'.out'
        problem = read_input(infile)
        problem.solution_3()
        output_file = open(outfile, 'w+')
        output_file.write(problem.output_sol())
        output_file.close()
