from Node import Node

WIDTH_OF_GRID = 10   # type: int
HEIGHT_OF_GRID = 10  # type: int

# constant list of nodes holding all the nodes on the grid
node_list = []

# initialize the starting node and the target node
# these variables will later point to a node inside the node list above
starting_node = Node(0,0)
target_node = Node(0,0)

# Create the list of nodes from the grid height and width
# The list will contains the nodes in order of columns starting from
# the left-most column and going up the column in y values
for x in range(WIDTH_OF_GRID):
    for y in range(HEIGHT_OF_GRID):
        new_node = Node(x, y)
        node_list.append(new_node)


def declare_starting_node(x,y):
    # from the x,y location, we can get the corresponding node in the list
    # given (x,y) = (0,5) we want the sixth element so index 5
    # given (x,y) = (1,5) we want the x * height + y ( i.e index 15 if height is 10)
    index = HEIGHT_OF_GRID * x + y
    # make the global variable start node point to the right index inside node list
    global starting_node
    starting_node = node_list[index]


def declare_target_node(x,y):
    # from the x,y location, we can get the corresponding node in the list
    # given (x,y) = (0,5) we want the sixth element so index 5
    # given (x,y) = (1,5) we want the x * height + y ( i.e index 15 if height is 10)
    index = HEIGHT_OF_GRID * x + y
    # make the global variable start node point to the right index inside node list
    global target_node
    target_node = node_list[index]


declare_starting_node(0, 0)
declare_target_node(WIDTH_OF_GRID - 2, HEIGHT_OF_GRID - 1)

starting_node.compute_g_and_h(starting_node, target_node)
target_node.compute_g_and_h(starting_node, target_node)

print(starting_node.x_cord)
print(starting_node.y_cord)
print(target_node.x_cord)
print(target_node.y_cord)
print("Empty line")
print(starting_node.g_value)
print(starting_node.h_value)
print(target_node.g_value)
print(target_node.h_value)










