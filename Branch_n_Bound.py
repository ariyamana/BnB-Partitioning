def initialize(chip, num_random_samples):

    from random import shuffle, choice
    from numpy import floor

    sample = 0
    best_assignment = {'left': [],'right': []}
    best_cost = chip.num_hyper_edges * 10**2

    while sample < num_random_samples:

        sample += 1

        temp_list = range(chip.num_nodes)

        shuffle(temp_list)

        half_mark = int(floor((chip.num_nodes)*1.0/2.0))

        random_assignment = {'left': temp_list[0:half_mark],\
        'right': temp_list[half_mark:]}

        # A stochastic greedy descent:
        for random_corrections in range(half_mark**2):
            node_left = choice(random_assignment['left'])
            node_right = choice(random_assignment['right'])

            delta = chip.swap_delta_cost(random_assignment,\
            node_left, node_right)

            if delta < 0:
                random_assignment['left'].remove(node_left)
                random_assignment['right'].remove(node_right)

                random_assignment['left'].append(node_right)
                random_assignment['right'].append(node_left)

        # Steepest Descent:
        while True:

            steepest_delta = 0
            steepest_left_node = -1
            steepest_right_node = -1

            for node_left in random_assignment['left']:
                for node_right in random_assignment['right']:

                    delta = chip.swap_delta_cost(random_assignment,\
                    node_left, node_right)

                    if delta < steepest_delta:
                        steepest_delta = delta
                        steepest_left_node = node_left
                        steepest_right_node = node_right


            if steepest_left_node != -1:

                random_assignment['left'].remove(steepest_left_node)
                random_assignment['right'].remove(steepest_right_node)

                random_assignment['left'].append(steepest_right_node)
                random_assignment['right'].append(steepest_left_node)

            else:
                break

        cost = chip.compute_cost(random_assignment)


        if cost < best_cost:
            best_assignment['left']  = [x for x in random_assignment['left']]
            best_assignment['right'] = [x for x in random_assignment['right']]
            best_cost = cost

    incumbent = {'bisection': best_assignment, 'cost': best_cost}

    next_node_first = chip.gen_next_node(None)

    new_assignment = {'left': [next_node_first],'right': []}

    next_node = chip.gen_next_node(next_node_first)

    counter = 0

    return incumbent, next_node, new_assignment, counter

def append_assignment(current_assignment, next_node, part):
    ''' This function amends a current assignment by adding one node to one of
    the partitions. In order to make sure a new part of the memory is used and
    the recursion algorithm runs flawlessly a for loop is used to make a deep
    copy of the current assignment and then ammending it with the new addition
    '''

    # Initialize the new assignment:
    new_assignment = {'left':[], 'right':[]}

    # First create a separate copy of the current assignment:
    for key in current_assignment.keys():
        for node in current_assignment[key]:
            new_assignment[key].append(node)

    # Now amend the separate copy with the new assignment:
    new_assignment[part].append(next_node)

    return new_assignment


def BnB(current_assignment, next_node, incumbent, chip, counter, verbose):

    #print 'Node:', next_node, '@cost:', incumbent['cost'] ,'...'

    if next_node == None: #Currently at a leaf
        counter += 1
        cost = chip.compute_cost(current_assignment)

        if cost < incumbent['cost']:
            print 'Cost improved to:' , cost , '@ decision tree node:', counter
            incumbent = {'bisection': current_assignment, 'cost': cost}

        return incumbent, counter
    else:
        '''Bounding -----------------------------------------------------'''
        # Given a partial solution calculate the lower bound of the current
        # branch:
        x_bound = chip.compute_partial_cost(current_assignment)
        #print x_bound, current_assignment['left'], current_assignment['right']
        #print 'x bound is:', x_bound , '@ counter:', counter

        '''Branching ----------------------------------------------------'''
        if x_bound < incumbent['cost']:
            #print 'node is:' , next_node
            '''Left branch'''
            # Expand the current assignment by appending the next_node to
            # the left Partition and call it temp_new_assignment:
            temp_new_assignment = append_assignment(current_assignment, \
            next_node, 'left')

            # Find the node after next_node and call it temp_next_node:
            temp_next_node = chip.gen_next_node(next_node)

            # Call the BnB with the current updates to the left partition:
            incumbent, counter = BnB(temp_new_assignment, temp_next_node,\
            incumbent, chip, counter, verbose)


            '''Right branch'''
            # Expand the current assignment by appending the next_node to
            # the right Partition and call it temp_new_assignment:
            temp_new_assignment = append_assignment(current_assignment, \
            next_node, 'right')

            # Find the node after next_node and call it temp_next_node:
            temp_next_node = chip.gen_next_node(next_node)

            # Call the BnB with the current updates to the right partition:
            incumbent, counter = BnB(temp_new_assignment, temp_next_node,\
            incumbent, chip, counter, verbose)

        else:
            if verbose > 1:
                print 'Pruned @ decision tree branch:', counter

            num_assigned_nodes = len(current_assignment['left'])+\
            len(current_assignment['right'])

            counter += 2 **(chip.num_nodes - num_assigned_nodes)


    return incumbent, counter


if __name__ =="__main__":

    import load as LD

    input_adress = 'Examples/z4ml.txt'

    chip1 = LD.load_input(input_adress, verbose =1)

    incumbent, next_node, new_assignment, counter = initialize(chip1, 200)

    solution = BnB(new_assignment, next_node, incumbent, chip1, counter, 1)

    print solution
