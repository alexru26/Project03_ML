import heapq
import matplotlib.pyplot as plt
import networkx as nx
import os
import pickle

def quick_draw(G):
    """
    Helper draw function
    :param G: the graph
    """
    pos = nx.shell_layout(G) # create shell layout
    nx.draw(G, pos, with_labels=True, font_weight='bold') # draw graph
    nx.draw_networkx_edge_labels( # draw the labels of the edges
        G,
        pos,
        edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    )
    plt.show() # show graph

def draw_with_path(G, path, path_edges):
    """
    Helper draw function with the outlined path
    :param G: the graph
    :param path: the path
    :param path_edges: the edges of the path
    """
    # pos = nx.spring_layout(G, seed=42)
    pos = nx.shell_layout(G) # create shell layout
    nx.draw(G, pos, with_labels=True, font_weight='bold')  # draw graph
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='r')  # highlight nodes
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=5)  # highlight path to take
    nx.draw_networkx_edge_labels( # draw the labels of the edges
        G,
        pos,
        edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    )

def setup():
    """
    Setup CLI to create/load/delete graph
    :return: the graph
    """
    choice = 0
    while True:
        print("*** Setup ***")
        print("1) Create new graph")
        print("2) Load graph")
        print("3) Delete graph")
        try:
            choice = int(input())
        except ValueError:
            print("Invalid input")
        print()

        if choice == 1: # create new graph
            return nx.Graph()

        elif len(os.listdir('../graphs')) != 0: # if there are existing graphs
            if choice == 2: # load graph
                print("Loading model...")
                graph_name = ""
                while not os.path.exists('../graphs/'+graph_name+'.pickle'):
                    graph_name = input("Enter graph name >>>")
                print()
                with open('../graphs/'+graph_name+'.pickle', 'rb') as f:
                    G = pickle.load(f)
                return G

            elif choice == 3: # delete graph
                print("Deleting model...")
                graph_name = ""
                while not os.path.exists('../graphs/'+graph_name+'.pickle'):
                    graph_name = input("Enter graph name >>>")
                os.remove('../graphs/'+graph_name+'.pickle')
                print()

def select_algorithm(G):
    """
    Select algorithm CLI to choose pathfinding algorithm
    :param G: the graph
    """
    choice = 0
    while choice != 2:
        print("*** Select algorithm ***")
        print("1) A*")
        print("2) Quit")
        try:
            choice = int(input())
        except ValueError:
            print("Invalid input")
        print()

        if choice == 1: # A*
            a_star(G)

def heuristic(node1, node2, pos):
    """
    Calculates the Euclidean distance between two nodes
    :param node1:
    :param node2:
    :param pos:
    :return:
    """
    (x1, y1), (x2, y2) = pos[node1], pos[node2]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def reconstruct_path(came_from, current):
    """

    :param came_from:
    :param current:
    :return:
    """
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    return path[::-1]

def a_star(G):
    """
    A* pathfinding algorithm
    :param G: the graph
    """
    # get start and end node
    start_node = -1
    end_node = -1
    while not G.has_node(start_node) or not G.has_node(end_node):
        try:
            start_node = int(input("Enter start node >>>"))
            end_node = int(input("Enter end node >>>"))
        except ValueError:
            print("Invalid input")

    pos = nx.shell_layout(G)  # get positioning of graph

    open_set = []
    heapq.heappush(open_set, (0, start_node))
    came_from = {start_node: None}
    g_score = {node: float('inf') for node in G.nodes}
    g_score[start_node] = 0
    f_score = {node: float('inf') for node in G.nodes}
    f_score[start_node] = heuristic(start_node, end_node, pos)

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end_node:
            path = reconstruct_path(came_from, current)
            break

        for neighbor in G.neighbors(current):
            tentative_g_score = g_score[current] + G[current][neighbor].get('weight', 1)

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end_node, pos)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    else:
        path = []
    path_edges = list(zip(path, path[1:]))

    draw_with_path(G, path, path_edges)

    plt.show()
    print()
    save = ''
    while save != 'y' and save != 'n':
        save = input("Would you like to save the image? (y/n) >>>")
    if save == 'y':
        image_name = input("Enter image name >>>")

        # Redraw graph
        draw_with_path(G, path, path_edges)

        # Save graph as img
        plt.savefig('../imgs/'+image_name+'.png')
        plt.close()

    print()

def main():
    """
    Main CLI to edit graph or run pathfinding algorithm
    """
    G = setup()

    choice = 0
    while choice != 6:

        quick_draw(G)

        print("*** Main ***")
        print("1) Add node")
        print("2) Add edge")
        print("3) Delete edge")
        print("4) Run pathfinding algorithm")
        print("5) Save graph")
        print("6) Quit")
        try:
            choice = int(input())
        except ValueError:
            print("Invalid input")
        print()

        if choice == 1: # add node
            G.add_node(G.number_of_nodes())

        elif G.number_of_nodes() != 0: # if there are nodes
            if choice == 2: # add edge
                node_1 = -1
                node_2 = -1
                weight = 0
                while not (G.has_node(node_1) and G.has_node(node_2) and weight > 0):
                    try:
                        node_1 = int(input("Enter node 1 >>>"))
                        node_2 = int(input("Enter node 2 >>>"))
                        weight = int(input("Enter weight >>>"))
                    except ValueError:
                        print("Invalid input")
                G.add_edge(node_1, node_2, weight=weight)
                print()

            elif choice == 3: # delete edge
                node_1 = -1
                node_2 = -1
                while not (G.has_node(node_1) and G.has_node(node_2) and G.has_edge(node_1, node_2)):
                    try:
                        node_1 = int(input("Enter node 1 >>>"))
                        node_2 = int(input("Enter node 2 >>>"))
                    except ValueError:
                        print("Invalid input")
                G.remove_edge(node_1, node_2)
                print()

            elif choice == 4: # select pathfinding algorithm
                select_algorithm(G)

            elif choice == 5: # save model
                print("Saving model...")
                graph_name = input("Enter graph name >>>")
                with open('../graphs/'+graph_name+'.pickle', 'wb') as f:
                    pickle.dump(G, f)
                print()

if __name__ == '__main__':
    """
    Main entry point
    """
    main()
