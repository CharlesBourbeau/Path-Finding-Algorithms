from tkinter import *
from AStarAlgorithm import AStarAlgorithm
from BreadthFirst import BreadthFirst


class Grid:

    def __init__(self, master, width, height):

        north_frame = Frame(master, height="100")
        north_frame.pack()

        top_frame = Frame(master, width=800, height=800, bg="black")
        top_frame.pack()

        bottom_frame = Frame(master, height=200, bg="white")
        bottom_frame.pack()

        self.string_dd = StringVar(master)
        self.string_dd.set("Choose Algorithm") # Default value

        self.options = ["A star", "Breadth First"]

        self.drop_down = OptionMenu(north_frame, self.string_dd, *self.options)
        self.drop_down.pack()

        self.find_path_button = Button(bottom_frame, text="Solve", command=self.start_solve)
        self.find_path_button.pack(side="left")

        self.reset_button = Button(bottom_frame, text="Reset", command=self.reset_all)
        self.reset_button.pack(side="left")

        self.labels = []

        for y in range(height):
            for x in range(width):
                row = height - y
                temp_label = Label(top_frame, name="label%d+%d" % (x, y), bg="white", height=2, width=5)
                temp_label.grid(row=row, column=x, padx=3, pady=3)
                temp_label.bind("<Button-1>", self.left_click)
                self.labels.append(temp_label)

    def left_click(self, event):
        caller = event.widget
        label_name = "%s" % caller

        # The name of a widget is always .!frame.label<x>+<y>, i.e. .!frame.label5+7
        # catch both digit group using regex
        pattern = '([0-9]+)\+([0-9]+)'
        match = re.search(pattern, label_name)

        x_pos = int(match.group(1))
        y_pos = int(match.group(2))

        caller.config(bg="grey20")

        # for breadth first search :

        # get the obstacle node from its x and y cord
        index = bfs.HEIGHT_OF_GRID * x_pos + y_pos
        new_obstacle = bfs.node_list[index]

        # now add the clicked node to the list of obstacle nodes
        bfs.obstacle_nodes.append(new_obstacle)

        # for the a star :

        index = a_star.HEIGHT_OF_GRID * x_pos + y_pos
        new_obstacle = a_star.node_list[index]

        a_star.obstacle_nodes.append(new_obstacle)

    def start_solve(self):
        # we need to see what option was chosen in the drop down menu
        option_chosen = g.string_dd.get()
        print(option_chosen)
        if option_chosen == g.options[0]:
            print("a star")
            # a star chosen
            a_star.a_star_algorithm()
            a_star.draw_path()

        if option_chosen == g.options[1]:
            print("breadth first")
            # breadth first
            bfs.build_tree_and_search()
            bfs.draw_path()

    def reset_all(self):
        # reset the grid colors
        for i in range(len(self.labels)):
            label_name = "%s" % self.labels[i]

            # The name of a widget is always .!frame.label<x>+<y>, i.e. .!frame.label5+7
            # catch both digit group using regex
            pattern = '([0-9]+)\+([0-9]+)'
            match = re.search(pattern, label_name)

            x_pos = int(match.group(1))
            y_pos = int(match.group(2))

            # get the obstacle node from its x and y cord
            global a_star
            index = a_star.HEIGHT_OF_GRID * x_pos + y_pos
            label_node = a_star.node_list[index]
            if label_node is not a_star.starting_node and label_node is not a_star.target_node:
                self.labels[i].config(bg="white", text="")

        # reset the a star algorithm
        for node in a_star.node_list:
            if node is not a_star.starting_node and node is not a_star.target_node:
                node.reset_node()

        a_star = AStarAlgorithm(root, g)
        a_star.declare_starting_node(0, 0)
        a_star.declare_target_node(15 - 1, 15 - 1)
        a_star.starting_node.compute_g_h_f(None, a_star.target_node)
        a_star.target_node.compute_g_h_f(None, a_star.target_node)

        # reset the breadth first algorithm

        bfs = BreadthFirst(root, g)
        bfs.declare_starting_node(0, 0)
        bfs.declare_target_node(bfs.WIDTH_OF_GRID - 1, bfs.HEIGHT_OF_GRID - 1)


root = Tk()

g = Grid(root, 15, 15)


a_star = AStarAlgorithm(root, g)
a_star.declare_starting_node(0, 0)
a_star.declare_target_node(15 - 1, 15 - 1)
a_star.starting_node.compute_g_h_f(None, a_star.target_node)
a_star.target_node.compute_g_h_f(None, a_star.target_node)


bfs = BreadthFirst(root, g)
bfs.declare_starting_node(0, 0)
bfs.declare_target_node(bfs.WIDTH_OF_GRID - 1, bfs.HEIGHT_OF_GRID - 1)


root.mainloop()

