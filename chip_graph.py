from numpy import floor,ceil
import matplotlib.pyplot as plt
import networkx as nx
from itertools import combinations

class chip_graph():
    def __init__(self, num_cells, num_conns, net_list):
        self.num_nodes = num_cells
        self.num_hyper_edges = num_conns
        self.hyperedge_set = net_list
        self.get_degrees()
        self.get_order()
        self.get_incident_dict()

    def compute_cost(self, assignment):
        cost = 0

        left  = set(assignment['left'])
        right = set(assignment['right'])

        if abs(len(left)-len(right)) == ((self.num_nodes) %2):

            for hyperedge in self.hyperedge_set:
                if not (set(hyperedge).issubset(left)):
                    if not (set(hyperedge).issubset(right)):
                        cost += 1

            return cost

        else:
            # Infeasible solution, return a big cost so that it is never
            # accepted as a better solution:
            return self.num_hyper_edges * 10**2

    def compute_partial_cost(self, assignment):

        partial_cost = 0

        left  = set(assignment['left'])
        right = set(assignment['right'])

        assigned_nodes = left.union(right)

        if abs(len(left)-len(right)) <= self.num_nodes-len(assigned_nodes):
            for hyperedge in self.hyperedge_set:
                if len(set(hyperedge).intersection(assigned_nodes))>= 2:

                    if not (set(hyperedge).issubset(left)):

                        if not (set(hyperedge).issubset(right)):

                            partial_cost += 1

        else:
            partial_cost = self.num_hyper_edges * 10**2


        return partial_cost

    def get_degrees(self):
        self.deg_dict = {}

        for hyper_edge in self.hyperedge_set:
            for node in hyper_edge:
                if node in self.deg_dict.keys():
                    self.deg_dict[node] = self.deg_dict[node]+1
                else:
                    self.deg_dict[node] = 1

    def get_order(self):

        self.sorted_deg_list =[]
        deg_list=[]

        for i in range(self.num_nodes):
            deg_list.append((i,self.deg_dict[i]))

        # Sort based on degrees:
        deg_list = sorted(deg_list, key=lambda x: x[1],reverse=True)

        for item in deg_list:
            self.sorted_deg_list.append(item[0])

        #print self.sorted_deg_list


    def get_incident_dict(self):

        self.incident_dict={}

        for i in range(self.num_hyper_edges):
            for node in self.hyperedge_set[i]:
                if node in self.incident_dict.keys():
                    self.incident_dict[node].append(i)
                else:
                    self.incident_dict[node]=[i]

    def gen_next_node(self, current_node):
        ''' Based on the following paper:

        W. W. Hager, D. T. Phan, and H. Zhang.
        An Exact Algorithm for Graph Partitioning. Mathematical Programming

        The order of visiting nodes can simply be based on the weight of the edges
        adjacent to that node. Here we can replace this by the degree of the node.
        '''
        if current_node != None:

            current_level = self.sorted_deg_list.index(current_node)
        else:
            current_level = -1

        if current_level < self.num_nodes-1:
            next_node = self.sorted_deg_list[current_level+1]
        else:
            next_node = None

        return next_node

    def draw_partition(self, assignment):

        G = nx.Graph()

        G.add_nodes_from(range(self.num_nodes))

        for hyper_edge in self.hyperedge_set:
            #for i in range(len(hyper_edge)-1):
            #    G.add_edge(hyper_edge[i],hyper_edge[i+1])

            for pair in combinations(set(hyper_edge), 2):
                G.add_edge(pair[0],pair[1])

        color_list=[]
        for node in G.nodes():
            if node in assignment['left']:
                color_list.append('#07B9F5')
            else:
                color_list.append('#F5075A')

        pos=nx.spring_layout(G, dim =2, iterations = 5000)

        nx.draw(G,pos, node_color = color_list, label= range(self.num_nodes))
        nx.draw_networkx_labels(G, pos, labels=None, font_size=12)
        plt.show()




if __name__ == "__main__":

    cg = chip_graph(5, 5, [[0,1],[1,2],[1,3],[1,3,4],[0,2,4]])

    cost = cg.compute_partial_cost({'left':[0,1,2,3,4],'right':[]})
    print cost
