def initialize(chip, max_iter):

    from random import shuffle, choice
    from numpy import floor

    temp_list = range(chip.num_nodes)

    shuffle(temp_list)

    half_mark = int(floor((chip.num_nodes)*1.0/2.0))

    new_assignment = {'left': [],'right': []}

    random_assignment = {'left': temp_list[0:half_mark],\
    'right': temp_list[half_mark:]}

    cost = chip.compute_cost(random_assignment)

    random_iter = 0

    while random_iter < max_iter:
        left_node = choice(random_assignment['left'])
        right_node = choice(random_assignment['right'])

        random_assignment['left'].remove(left_node)
        random_assignment['left'].append(right_node)

        random_assignment['right'].remove(right_node)
        random_assignment['right'].append(left_node)

        temp_cost = chip.compute_cost(random_assignment)

        if temp_cost > cost:
            random_assignment['left'].remove(right_node)
            random_assignment['left'].append(left_node)

            random_assignment['right'].remove(left_node)
            random_assignment['right'].append(right_node)
        else:
            cost = temp_cost

        random_iter += 1





    next_node = chip.gen_next_node(None)

    incumbent = {'bisection': random_assignment, 'cost': cost}

    print 'Initial bisection cost:', incumbent['cost']
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


def BnB(current_assignment, next_node, incumbent, chip, counter):

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
            incumbent, chip, counter)


            '''Right branch'''
            # Expand the current assignment by appending the next_node to
            # the right Partition and call it temp_new_assignment:
            temp_new_assignment = append_assignment(current_assignment, \
            next_node, 'right')

            # Find the node after next_node and call it temp_next_node:
            temp_next_node = chip.gen_next_node(next_node)

            # Call the BnB with the current updates to the right partition:
            incumbent, counter = BnB(temp_new_assignment, temp_next_node,\
            incumbent, chip, counter)

        else:

            #print 'branch pruned.'

            num_assigned_nodes = len(current_assignment['left'])+\
            len(current_assignment['right'])

            counter += 2 **(chip.num_nodes - num_assigned_nodes)


    return incumbent, counter


if __name__ =="__main__":

    import load as LD

    input_adress = 'Examples/twocm.txt'

    chip1 = LD.load_input(input_adress, verbose =1)

    incumbent, next_node, new_assignment, counter = initialize(chip1, 300)

    solution = BnB(new_assignment, next_node, incumbent, chip1, counter)

    print solution
