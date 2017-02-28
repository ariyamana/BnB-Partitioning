
def amend_assignment(current_assignment, node, part):
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

def BnB(current_assignment, next_node, incumbent):
    if next_node == null: #Currently at a leaf
        if this is the best solution so far:
            store the current solution
        else:

            calculate label x

            if x < incumbent:
                '''Left'''
                # Expand the current assignment by appending the next_node to
                # the left Partition and call it temp_new_assignment:
                temp_new_assignment = amend_assignment(current_assignment, \
                next_node, 'left')

                # Branching:
                # Find the node after next_node and call it temp_next_node:

                # Call the BnB with the current updates to the left partition:
                BnB(temp_new_assignment, temp_next_node, incumbent)


                '''Right'''
                # Expand the current assignment by appending the next_node to
                # the right Partition and call it temp_new_assignment:
                temp_new_assignment = amend_assignment(current_assignment, \
                next_node, 'right')

                # Branching:
                # Find the node after next_node and call it temp_next_node:

                # Call the BnB with the current updates to the right partition:
                BnB(temp_new_assignment, temp_next_node, incumbent)
