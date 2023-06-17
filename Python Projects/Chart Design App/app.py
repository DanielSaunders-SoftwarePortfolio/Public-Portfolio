import tkinter as tk
from shapes import *

class PropertyPane:
    def __init__(self, master, draw_func, width=200, height=200, row=1, col=0) -> None:
        self.frame     = tk.Frame(master, width=width, height=height)
        self.master    = master
        self.row       = row
        self.col       = col
        self.draw_func = draw_func
        self.showing   = False
        
        self.frame.grid(row=row, column=col)
        
    def display_properties(self, shape:Shape):
        self.clear()
        self.frame.grid(row=1, column=0)
        self.showing = True
        
        self.properties_label = tk.Label(self.frame, text="Shape Properties:")
        self.properties_label.grid(row=0, column=0, columnspan=2)
        
        self.shape_type_label = tk.Label(self.frame, text="Title:")
        self.shape_type_label.grid(row=1, column=0)
        self.shape_title_entry = tk.Entry(self.frame)
        self.shape_title_entry.insert(tk.END, shape.label)
        self.shape_title_entry.grid(row=1, column=1)
        
        self.x_label = tk.Label(self.frame, text="X")
        self.x_label.grid(row=2, column=0)
        self.x_entry = tk.Entry(self.frame)
        self.x_entry.insert(tk.END, str(shape.x))
        self.x_entry.grid(row=3, column=0)

        self.y_label = tk.Label(self.frame, text="Y")
        self.y_label.grid(row=2, column=1)
        self.y_entry = tk.Entry(self.frame)
        self.y_entry.insert(tk.END, str(shape.y))
        self.y_entry.grid(row=3, column=1)
        
        self.span_lable1 = tk.Label(self.frame, text=" ")
        self.span_lable1.grid(row=4, column=0, columnspan=2)

        self.width_label = tk.Label(self.frame, text="Width:")
        self.width_label.grid(row=5, column=0)
        self.width_entry = tk.Entry(self.frame)
        self.width_entry.insert(tk.END, str(shape.width))
        self.width_entry.grid(row=5, column=1)
        
        self.height_label = tk.Label(self.frame, text="Height:")
        self.height_label.grid(row=6, column=0)
        self.height_entry = tk.Entry(self.frame)
        self.height_entry.insert(tk.END, str(shape.height))
        self.height_entry.grid(row=6, column=1)
        
        self.span_lable2 = tk.Label(self.frame, text=" ")
        self.span_lable2.grid(row=7, column=0, columnspan=2)
        
        # Bind a button click event to update the shape properties
        self.update_button = tk.Button (
                                        self.frame, text="Update", 
                                        command=lambda: 
                                            self.update_shape_properties(
                                                shape, 
                                                self.shape_title_entry.get(),
                                                self.x_entry.get(), 
                                                self.y_entry.get(), 
                                                self.width_entry.get(), 
                                                self.height_entry.get()
                                            )
                                       )
        self.update_button.grid(row=8, column=0, columnspan=2)
        
    def clear(self):
        self.showing=False
        self.frame.destroy()
        self.frame = tk.Frame(self.master, width=200, height=200)
    
    def update_coordinates(self, x, y):
        if self.showing:
            self.y_entry.delete(0,tk.END)
            self.x_entry.delete(0,tk.END)
            
            self.y_entry.insert(0,str(y))
            self.x_entry.insert(0,str(x))
            
    
    def update_shape_properties(self, shape:Shape, label, x, y, width, height):
        # Update the selected shape properties
        shape.label = label
        shape.x = int(x)
        shape.y = int(y)
        shape.width = int(width)
        shape.height = int(height)
        self.draw_func()
        self.display_properties(shape)
        

class App:
    def __init__(self):
        self.shapes = []
        self.selected_shape = None

        self.root = tk.Tk()
        self.root.title("Chart App")

        self.menu_panel = tk.Frame(self.root, width=200, height=200)
        self.menu_panel.grid(row=0, column=0)

        self.view_panel = tk.Canvas(self.root, bg="white", width=700, height=400)
        self.view_panel.grid(row=0, column=1, rowspan=2, sticky="nsew")
        
        self.edit_panel = PropertyPane(self.root, self.draw_shapes, width=200, height=200, row=1, col=0)

        Rectangle_button = tk.Button(self.menu_panel, text="Rectangle", command=self.create_Rectangle)
        Rectangle_button.pack()

        circle_button = tk.Button(self.menu_panel, text="Circle", command=self.create_circle)
        circle_button.pack()

        rounded_rect_button = tk.Button(self.menu_panel, text="Rounded Rectangle", command=self.create_rounded_rect)
        rounded_rect_button.pack()

        diamond_button = tk.Button(self.menu_panel, text="Diamond", command=self.create_diamond)
        diamond_button.pack()

        self.view_panel.bind("<Button-1>", self.select_shape)
        self.view_panel.bind("<B1-Motion>", self.move_shape)

    def create_Rectangle(self):
        
        rectangle = Rectangle(50, 50, 100, 150)
        index = len(self.shapes)
        rectangle.change_label("Process "+str(index))
        self.shapes.append(rectangle)
        self.draw_shapes()

    def create_circle(self):
        circle = Circle(50, 50, 100, 100)
        index = len(self.shapes)
        circle.change_label("Circle "+str(index))
        self.shapes.append(circle)
        self.draw_shapes()

    def create_rounded_rect(self):
        rounded_rect = RoundedRectangle(50, 50, 75, 150)
        index = len(self.shapes)
        rounded_rect.change_label("Terminator "+str(index))
        self.shapes.append(rounded_rect)
        self.draw_shapes()

    def create_diamond(self):
        diamond = Diamond(50, 50, 100, 150)
        index = len(self.shapes)
        diamond.change_label("Decision "+str(index))
        self.shapes.append(diamond)
        self.draw_shapes()

    def draw_shapes(self):
        self.view_panel.delete("all")
        for shape in self.shapes:
            shape.draw(self.view_panel, self.selected_shape==shape)

    def select_shape(self, event):
        x, y = event.x, event.y
        selected_shape = None
        for shape in self.shapes:
            if shape.contains_point(x, y) and shape != self.selected_shape:
                selected_shape = shape
                break
            
        if selected_shape:
            self.selected_shape = selected_shape
            selected_shape.start_mod(x, y)
        else:
            if self.selected_shape:
                if not self.selected_shape.contains_point(x, y):
                    self.selected_shape = None
                    self.edit_panel.clear()
        
        if self.selected_shape:
            self.show_shape_properties()
        
        self.draw_shapes()

    def show_shape_properties(self):
        if self.selected_shape:
            self.edit_panel.display_properties(self.selected_shape)

    def move_shape(self, event):
        
        if self.selected_shape!=None:
            # print("moving shape")
            shape = self.selected_shape
            x, y, = event.x, event.y
            shape.move(x, y)
            self.draw_shapes()
            self.edit_panel.update_coordinates(shape.x, shape.y)
    
    def run(self):
        self.root.mainloop()
            
