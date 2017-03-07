import load as LD
import os
import Branch_n_Bound as BB
import time

def run_directory(directory, heuristic, verbose):
    os.system('clear')

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_address = os.path.join(directory, filename)



            loaded_chip = LD.load_input(file_address, verbose =1)

            incumbent, next_node, new_assignment, counter =\
            BB.initialize(loaded_chip, heuristic)

            print 'Branch and Bound started ...'

            time1 = time.time()

            solution, counter = BB.BnB(new_assignment, next_node, incumbent,\
            loaded_chip, counter)

            time2 = time.time()

            if counter == 2**loaded_chip.num_nodes:
                print 'Branch and Bound finished in', time2-time1, 'seconds.'
                print 'Optimal solution cost:', solution['cost']
                if verbose > 1:
                    loaded_chip.draw_partition(solution['bisection'])
            else:
                print 'Warning! for some reason some nodes of the decision',
                print 'tree were not explored (neither pruned nor searched).'
                print 'Branch and Bound exited in', time2-time1, 'seconds.'
                print 'Best solution cost:', solution['cost']




if __name__ == "__main__":

    address = 'Examples'
    os.system('clear')

    print '='*80
    print 'Branch&Bound-based Bisection'
    print 'Developed by: Arman Zaribafiyan'
    print 'Assignment 3 for course EECE 583'
    print '-'*80
    print 'NOTE: This algorithm runs over all input files in the',
    print 'Examples folder.'
    print '='*80
    print 'The algorithm uses a random correction heuristic for',
    print 'intial bi-partition'

    heuristic_iterations = \
    raw_input('>>> Random Correction Heuristic Iterations: ')

    visualize = raw_input('Visualize Final Solution? [Yes/No] ')
    if visualize =='Yes':
        verbose = 2
    else:
        verbose = 0

    run_directory(address, int(heuristic_iterations), verbose)
