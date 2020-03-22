from sys import maxsize
import time

class Node():
    """A node class for A* Pathfinding"""
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []
    # Add the start node
    open_list.append(start_node)
    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue
            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            # Create new node
            new_node = Node(current_node, node_position)
            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue
            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = round(((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2) ** 0.5)
            child.f = child.g + child.h
            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            # Add the child to the open list
            open_list.append(child)
# implementation of traveling Salesman Problem
def travellingSalesmanProblem(graph, s, V):
    # store all vertex apart from source vertex
    vertex = []
    for i in range(V):
        if i != s:
            vertex.append(i)
            # store minimum weight Hamiltonian Cycle
    min_path = maxsize
    list_path = []

    while True:
        # store current Path weight(cost)
        current_pathweight = 0
        # compute current path weight
        k = s
        list_path_temp = []
        for i in range(len(vertex)):
            current_pathweight += graph[k][vertex[i]]
            list_path_temp.append(vertex[i])
            k = vertex[i]
        current_pathweight += graph[k][s]
        # update minimum
        if current_pathweight < min_path:
            min_path = current_pathweight
            list_path = list_path_temp

        if not next_permutation(vertex):
            break
    return min_path, list_path

# next_permutation implementation
def next_permutation(L):
    n = len(L)
    i = n - 2
    while i >= 0 and L[i] >= L[i + 1]:
        i -= 1
    if i == -1:
        return False
    j = i + 1
    while j < n and L[j] > L[i]:
        j += 1
    j -= 1
    L[i], L[j] = L[j], L[i]
    left = i + 1
    right = n - 1

    while left < right:
        L[left], L[right] = L[right], L[left]
        left += 1
        right -= 1

    return True

# Driver Code
if __name__ == "__main__":

    starttime = time.time()
    with open("environment.txt", "r") as f:
        text_environment = f.read()

    environment = text_environment.split("\n")[3:13]
    st_point = text_environment.split("\n")[14].split(" ")  # read start position from environment.txt file
    #coords_list is the list of coordinat cookies
    coords_list = [(int(st_point[1]) - 1, int(st_point[2]) - 1)]  # add only start position (start position define as cookie)
    # print(environment)
    # print(st_point)
    block_list = [] # [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1,...]] list of lists 1 is block 0 free or cookie
    for Y, line in enumerate(environment):
        sep_line = line.split(" ")
        temp_list = []
        for X in range(len(sep_line)):
            if int(sep_line[X]) == 2:
                coords_list.append((int(Y), int(X)))
            if int(sep_line[X]) == 1:
                temp_list.append(1)
            else:
                temp_list.append(0)
        block_list.append(temp_list)
    # print("block list ", block_list)
    # print("coords list ", coords_list)

    graph = [] #[[0, 10, 4, 3, 2, 2, 4, 4, 3], [10, 0, ...]] distance from current cookies to other cookies
    for i in range(len(coords_list)):
        p = coords_list[i]
        temp = []
        for c in coords_list:
            Xcost = abs(c[0] - p[0])
            Ycost = abs(c[1] - p[1])
            temp.append(Xcost + Ycost)
        graph.append(temp)

    s = 0 #start position
    V = len(graph) #count of cookie
    print("graph ", graph)
    cost_min, list_minn = travellingSalesmanProblem(graph, s, V)
    # print("cost_min ",cost_min)
    list_minn.insert(0, s)
    print("list minn",list_minn)

    list_path_move = []
    start = coords_list[list_minn[0]]
    for vertixe in range(1, len(list_minn)):
        end = coords_list[list_minn[vertixe]]
        path = astar(block_list, start, end)
        start = end
        list_path_move.append(path)
    print("LIST PATH MOVE ", list_path_move)

    commands = []
    move_dict = {"top":0, "down":1, "right":2, "left":3}
    for path_to_cookie in list_path_move:
        for i in range(len(path_to_cookie) - 1):
            current_position = path_to_cookie[i]
            next_position = path_to_cookie[i+1]
            X1 = current_position[1]
            Y1 = current_position[0]
            X2 = next_position[1]
            Y2 = next_position[0]

            if Y1 > Y2:
                commands.append(move_dict["top"])
            if Y1 < Y2:
                commands.append(move_dict["down"])
            if X1 > X2:
                commands.append(move_dict["left"])
            if X1 < X2:
                commands.append(move_dict["right"])

    with open("optimalPath.txt", "w") as f:
        f.write(str(commands))

    stoptime = time.time()
    print("time spent ", stoptime - starttime)
    print("commands ",commands)
    print("len commands ", len(commands))
