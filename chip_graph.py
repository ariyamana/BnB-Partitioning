class chip_graph():
    def __init__(num_cells, num_conns, net_list):
        self.num_nodes = num_cells
        self.num_hyper_edges = num_conns
        self.hyperedge_set = net_list

    def compute_cost(assignment):
        cost = 0

        left  = set(assignment['left'])
        right = set(assignment['right'])

        for hyperedge in self.hyperedge_set:
            if ~(set(hyperedge).issubset(left)):
                if ~(set(hyperedge).issubset(right)):
                    cost += 1

        return cost
