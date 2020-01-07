from tkinter import *


class Grid:

    def __init__(self, master, width, height):
        frame = Frame(master, width=800, height=800, bg="black")
        frame.pack()

        self.labels = []

        for y in range(height):
            for x in range(width):
                row = height - y
                temp_label = Label(frame, name="label%d%d" % (x, y), text="(%d,%d)" % (x, y), bg="red", height=2, width=5)
                temp_label.grid(row=row, column=x, padx=3, pady=3)
                temp_label.bind("<Button-1>", self.leftclick)
                self.labels.append(temp_label)

    def leftclick(self, event):
        x_pos = event.x
        y_pos = event.y
        caller = event.widget
        print("(%d,%d)" % (x_pos, y_pos))
        print("widget= %s" % caller)
        caller.config(bg="white")

