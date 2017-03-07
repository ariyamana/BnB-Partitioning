import load as LD
import os
import Branch_n_Bound as BB
import time

def run_directory(directory, heuristic, verbose, prune_info):
    os.system('clear')

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_address = os.path.join(directory, filename)



            loaded_chip = LD.load_input(file_address, verbose =1)

            print 'Random Sampling + Steepest Descent ...',

            time01 = time.time()

            incumbent, next_node, new_assignment, counter =\
            BB.initialize(loaded_chip, heuristic)

            time02 = time.time()

            print 'Done in ', time02-time01, 'seconds'
            print 'Initial bisection cost:', incumbent['cost']

            print 'Branch and Bound started ...'

            time1 = time.time()

            solution, counter = BB.BnB(new_assignment, next_node, incumbent,\
            loaded_chip, counter, prune_info)

            time2 = time.time()



            print 'Branch and Bound finished in', time2-time1, 'seconds.'
            print '.'*80
            print 'Optimal solution cost:', solution['cost']
            print 'Total time:', time2-time1 + time02-time01
            print '\n'

            if verbose > 1:
                loaded_chip.draw_partition(solution['bisection'])






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


    heuristic_iterations = \
    raw_input('Number of Initial Random Samples: ')

    visualize = raw_input('Visualize Final Solution? [Yes/No] ')
    if visualize =='Yes':
        verbose = 2
    else:
        verbose = 0

    Pruning_log = raw_input('Display Pruning Info? [Yes/No] ')
    if Pruning_log =='Yes':
        show_prune = 2
    else:
        show_prune = 0

    run_directory(address, int(heuristic_iterations), verbose, show_prune)
