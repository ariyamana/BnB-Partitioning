def initialize():
    new_assignment = None
    cost = None
    incumbent = {'bisection': new_assignment, 'cost': cost}
    
def append_assignment(current_assignment, node, part):
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
    new_assignment[part].append(node)

    return new_assignment

def gen_next_node(current_assignment):



def BnB(current_assignment, next_node, incumbent, chip):
    if next_node == null: #Currently at a leaf

        cost = chip.compute_cost(current_assignment)

        if cost < incumbent['cost']:
            incumbent = {'bisection': current_assignment, 'cost': cost}

        else:
            '''Bounding -----------------------------------------------------'''
            # Given a partial solution calculate the lower bound of the current
            # branch:
            x_bound = ???

            '''Branching ----------------------------------------------------'''
            if x_bound < incumbent:
                '''Left branch'''
                # Expand the current assignment by appending the next_node to
                # the left Partition and call it temp_new_assignment:
                temp_new_assignment = append_assignment(current_assignment, \
                next_node, 'left')

                # Find the node after next_node and call it temp_next_node:
                temp_next_node =

                # Call the BnB with the current updates to the left partition:
                BnB(temp_new_assignment, temp_next_node, incumbent)


                '''Right branch'''
                # Expand the current assignment by appending the next_node to
                # the right Partition and call it temp_new_assignment:
                temp_new_assignment = append_assignment(current_assignment, \
                next_node, 'right')

                # Find the node after next_node and call it temp_next_node:

                # Call the BnB with the current updates to the right partition:
                BnB(temp_new_assignment, temp_next_node, incumbent)
