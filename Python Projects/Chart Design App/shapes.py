import tkinter as tk

STROKE_COLOR = "black"
SELECTED_STROKE = "red"
STROKE_WIDTH = 2
FILL_COLOR   = "white"
NODE_STROKE = "grey"

class Node:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.radius = 5
        
    def draw(self, canvas:tk.Canvas):
        x0 = self.x - self.radius
        y0 = self.y - self.radius
        x1 = self.x + self.radius
        y1 = self.y + self.radius
        
        canvas.create_oval(
                            x0, y0, 
                            x1, y1, 
                            outline = NODE_STROKE, 
                            width=1,
                            fill=FILL_COLOR
                           )

class Shape:
    '''
    Shape defines a polygon that can be drawn on a tkinter Canvas.
    '''
    def __init__(self, shape_type:str, x:int, y:int, height:int, width:int):
        '''
        Initialize and define the shape.
        parameters x and y define the center point of the shape.
        Width and height describe the full width and full height 
        of the shape, not the radius or halfwidth of the shape.
        shape_type is a constant that cannot be changed after initialization.
        '''
        # Position
        self.x = x
        self.y = y
        
        # Dimensions
        self.height = height
        self.width = width
        
        # Descritpions
        self.label = ""
        self._shape_type = shape_type
        
        # Nodes
        self.generate_nodes()

    def contains_point(self, x, y):
        '''
        Check if the point at the provided x and y is within the bounding box 
        of this shape.
        '''
        x_min = self.x-self.width//2 
        x_max = self.x + self.width//2
        x_in_range = x_min <= x and x <= x_max
        
        y_min = self.y-self.height//2 
        y_max = self.y + self.height//2
        y_in_range = y_min <= y and y <= y_max
        
        return x_in_range and y_in_range
    
    def draw(self, canvas:tk.Canvas, active:bool, smooth=False):
        '''
        Draws shape based on self.nodes. 
        
        If a shape is drawn as active, it will have a red outline and its nodes
        will be drawn. otherwise it will have a black background and no visible
        nodes.
        
        If smooth is chosen (True), then a bezier curve will be generated 
        between each node, otherwise, a straight line will be drawn between 
        each node.
        '''
        points = []
        if active: self.generate_nodes()
        for node in self.nodes:
            # Get points from nodes
            points.append(node.x)
            points.append(node.y)
        
        if not active:
            # Draw as inactive
            canvas.create_polygon(
                points,
                outline = STROKE_COLOR, width=STROKE_WIDTH,
                fill=FILL_COLOR, smooth=smooth
            )
        else:
            # Draw as active
            canvas.create_polygon(
                points,
                outline = SELECTED_STROKE, width=STROKE_WIDTH,
                fill=FILL_COLOR, smooth=smooth
                )   
            for node in self.nodes:
                # draw nodes for active shapes.
                node.draw(canvas)
                
        # Draw label text.
        self.draw_text(canvas)
    
    def change_label(self, new_text):
        '''
        Set label to a new string.
        '''
        self.label = new_text
        
    def add_to_label(self, text_to_add):
        '''
        Append text to the end of self.label
        '''
        self.label += text_to_add
    
    def backspace(self):
        '''
        Remove the last charachter from self.label
        '''
        # This is not currently used in the app. 
        self.label = self.label[:-1]
        
    def draw_text(self, canvas:tk.Canvas):
        '''
        Draw self.label on provided tkinter Canvas.
        '''
        canvas.create_text(self.x, self.y, text=self.label, anchor="center" )
    
    def start_mod(self, x, y):
        '''
        Saves the current state so that the user can cancel out of the mod.
        '''
        # Original State
        self.old_x = self.x
        self.old_y = self.y
        self.old_text = self.label
        
        # Initial mouse position 
            # Saving the mouse position at the start lets me measure
            # how far the mouse has moved from the start so that I can
            # mimic that movement with the shape's x and y positions.
        self.mod_x = x
        self.mod_y = y

    def move(self, x, y):
        '''
        Move the shape to the x and y postion provided
        if mod_x and mod_y are set, they will offset the 
        new shape position.
        '''
        if self.mod_x and self.mod_y:
            self.x = self.old_x + (x - self.mod_x)
            self.y = self.old_y + (y - self.mod_y)
        else:
            self.x = x
            self.y = y
        
    def generate_nodes(self):
        '''
        Generate nodes at shape corners and midpoints.
        '''
        x, y = self.x, self.y
        width, height = self.width//2, self.height//2
        self.nodes = []
        
        # Top Left Corner
        self.nodes.append(Node(x-width, y-height))
        # top Midpoint
        self.nodes.append(Node(x      , y-height))
        # Top Right Corner
        self.nodes.append(Node(x+width, y-height))
        # Right Midpoint
        self.nodes.append(Node(x+width, y       ))
        # Bottom Right Corner
        self.nodes.append(Node(x+width, y+height))
        # Bottom Midpoint
        self.nodes.append(Node(x      , y+height))
        # Bottom Left Corner
        self.nodes.append(Node(x-width, y+height))
        # Left Midbpoint
        self.nodes.append(Node(x-width, y       ))

class PropertyPanel(tk.Frame):
    '''
    PropertyPanel is a Frame designed to display and edit the properties of a shape.
    '''
    def __init__(self, root, draw_func, width=200, height=200, row=1, col=0) -> None:
        '''
        Root is the parent object of the PropertyPanel
        draw_func is the function used to draw the active chart
        width and height are the dimensions of the panel
        row and col are the grid row and col to display panel at in root
        '''
        super().__init__(root, width=width, height=height)
        self.root    = root
        self.row       = row
        self.col       = col
        self.draw_func = draw_func
        self.showing   = False
        
        self.grid(row=row, column=col)
        
    def display_properties(self, shape:Shape):
        '''
        Creates and populates fields within the Panel for each property of the
        provided shape.
        '''
        # In the future I may add a Shape method to get a list of properties 
        # so that the panel can be more dynamic.
        
        self.children.clear()
        self.grid(row=self.row, column=self.col)
        self.showing = True
        
        self.properties_label = tk.Label(self, text="Shape Properties:")
        self.properties_label.grid(row=0, column=0, columnspan=2)
        
        self.shape_type_label = tk.Label(self, text="Title:")
        self.shape_type_label.grid(row=1, column=0)
        self.shape_title_entry = tk.Entry(self)
        self.shape_title_entry.insert(tk.END, shape.label)
        self.shape_title_entry.grid(row=1, column=1)
        
        self.x_label = tk.Label(self, text="X")
        self.x_label.grid(row=2, column=0)
        self.x_entry = tk.Entry(self)
        self.x_entry.insert(tk.END, str(shape.x))
        self.x_entry.grid(row=3, column=0)

        self.y_label = tk.Label(self, text="Y")
        self.y_label.grid(row=2, column=1)
        self.y_entry = tk.Entry(self)
        self.y_entry.insert(tk.END, str(shape.y))
        self.y_entry.grid(row=3, column=1)
        
        self.span_lable1 = tk.Label(self, text=" ")
        self.span_lable1.grid(row=4, column=0, columnspan=2)

        self.width_label = tk.Label(self, text="Width:")
        self.width_label.grid(row=5, column=0)
        self.width_entry = tk.Entry(self)
        self.width_entry.insert(tk.END, str(shape.width))
        self.width_entry.grid(row=5, column=1)
        
        self.height_label = tk.Label(self, text="Height:")
        self.height_label.grid(row=6, column=0)
        self.height_entry = tk.Entry(self)
        self.height_entry.insert(tk.END, str(shape.height))
        self.height_entry.grid(row=6, column=1)
        
        self.span_lable2 = tk.Label(self, text=" ")
        self.span_lable2.grid(row=7, column=0, columnspan=2)
        
        # Bind a button click event to update the shape properties
        self.update_button = tk.Button (
                                        self, text="Update", 
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
        '''
        Clear out the properties displayed in the Panel
        '''
        self.showing=False
        self.children.clear()
    
    def update_coordinates(self, x, y):
        '''
        Update only the coordinates of the Panel
        '''
        if self.showing:
            self.y_entry.delete(0,tk.END)
            self.x_entry.delete(0,tk.END)
            
            self.y_entry.insert(0,str(y))
            self.x_entry.insert(0,str(x))
            
    def update_shape_properties(self, shape:Shape, label, x, y, width, height):
        '''
        Update the selected shape properties
        '''
        
        shape.label = label
        shape.x = int(x)
        shape.y = int(y)
        shape.width = int(width)
        shape.height = int(height)
        self.draw_func()
        self.display_properties(shape)

class Process(Shape):
    def __init__(self, x, y, height, width):
        super().__init__("Rectangle", x, y, height, width)
        self.generate_nodes()

class FlowNode(Shape):
    def __init__(self, x, y, height, width):
        super().__init__("Circle", x, y, height, width)

    def contains_point(self, x, y):
        x_distance = (self.x-x)/(self.width/2)
        y_distance = (self.y-y)/(self.height/2)
        return (x_distance)**2 + (y_distance)**2 <= 1
    
    def draw(self, canvas, active):
        super().draw(canvas, active, smooth=True)
        
    def generate_nodes(self):
        x, y = self.x, self.y
        width, height = self.width//2, self.height//2
        self.nodes = []
        half_x_rad = (2**0.5) * width//2
        half_y_rad = (2**0.5) * height//2
                
        self.nodes.append(Node(x-half_x_rad, y-half_y_rad))
        self.nodes.append(Node(x           , y-height           ))
        self.nodes.append(Node(x+half_x_rad, y-half_y_rad))
        self.nodes.append(Node(x+width     , y                  ))
        self.nodes.append(Node(x+half_x_rad, y+half_y_rad))
        self.nodes.append(Node(x           , y+height           ))
        self.nodes.append(Node(x-half_x_rad, y+half_y_rad))
        self.nodes.append(Node(x-width     , y                  ))

class Terminator(Shape):
    def __init__(self, x, y, height, width):
        super().__init__("Rounded Rectangle", x, y, height, width)
    
    def draw(self, canvas, active):
        half_width = self.width//2
        half_height = self.height//2
        x = self.x
        y = self.y
        radius = 3*self.height//8
        half_rad = radius//3
        points = [
                    # start curve
                    x - half_width + half_rad, y + half_height - half_rad,
                    x - half_width           , y,  # Corner
                    x - half_width + half_rad, y - half_height + half_rad,
                    # Start edge
                    x - half_width + radius , y - half_height,
                    x - half_width//3        , y - half_height,
                    x                        , y - half_height,
                    x + half_width//3        , y - half_height,
                    x + half_width - radius  , y - half_height,
                    # Start curve
                    x + half_width - half_rad, y - half_height + half_rad,
                    x + half_width           , y, # Corner
                    x + half_width - half_rad, y + half_height - half_rad,
                    # Start edge
                    x + half_width - radius  , y + half_height,
                    x + half_width//3        , y + half_height,
                    x                        , y + half_height,
                    x - half_width//3        , y + half_height,
                    x - half_width + radius  , y + half_height,
                  ]
        if not active:
            canvas.create_polygon(
                points, outline=STROKE_COLOR, width=STROKE_WIDTH,
                fill=FILL_COLOR, smooth=True
            )
        else:
            self.generate_nodes()
            canvas.create_polygon(
                points, outline=SELECTED_STROKE, width=STROKE_WIDTH,
                fill=FILL_COLOR, smooth=True
            )   
            for node in self.nodes:
                node.draw(canvas)
                
        self.draw_text(canvas)

    def generate_nodes(self):
        x, y = self.x, self.y
        width, height = self.width//2, self.height//2
        self.nodes = []
        radius = 3*height//8
        half_rad = radius//3
        
        self.nodes.append(Node(x-width+half_rad, y-height+half_rad))
        self.nodes.append(Node(x               , y-height         ))
        self.nodes.append(Node(x+width-half_rad, y-height+half_rad))
        self.nodes.append(Node(x+width         , y                ))
        self.nodes.append(Node(x+width-half_rad, y+height-half_rad))
        self.nodes.append(Node(x               , y+height         ))
        self.nodes.append(Node(x-width+half_rad, y+height-half_rad))
        self.nodes.append(Node(x-width         , y                ))
        
class Decision(Shape):
    '''
    A Diamond representing a decision in a Flow Chart
    '''
    def __init__(self, x, y, height, width):
        super().__init__("Diamond", x, y, height, width)

    def get_width_at_y(self, y):
        center_y = self.y
        half_height = self.height / 2
        if center_y - half_height < y and center_y + half_height > y:
            
            # the ratio gives us the percent of the half_height that y is away 
            # from center_y. We can then multiply that by the maximum width
            # of the diamond to get the actual width of the diamond at that height
            ratio = 1-(abs(y-center_y)/half_height)
            return self.width * ratio
        
        else: 
            return 0
    
    def contains_point(self, x, y):
        center_x = self.x
        half_width_at_height = self.get_width_at_y(y)//2
        if half_width_at_height != 0:
            if center_x - half_width_at_height < x and center_x + half_width_at_height > x:
                return True
        return False
        
    def draw(self, canvas, active):
        self.generate_nodes()
        if not active:
            canvas.create_polygon(
                self.x               , self.y + self.height/2,
                self.x + self.width/2, self.y,
                self.x               , self.y - self.height/2,
                self.x - self.width/2, self.y, 
                outline = STROKE_COLOR, width=STROKE_WIDTH,
                fill=FILL_COLOR
            )
        else:
            canvas.create_polygon(
            self.x               , self.y + self.height/2,
            self.x + self.width/2, self.y,
            self.x               , self.y - self.height/2,
            self.x - self.width/2, self.y, 
            outline = SELECTED_STROKE, width=STROKE_WIDTH,
            fill=FILL_COLOR
            )   
            for node in self.nodes:
                node.draw(canvas)
                
        self.draw_text(canvas)
        
    def generate_nodes(self):
        x, y = self.x, self.y
        width, height = self.width//2, self.height//2
        self.nodes = []
        
        # Top Left Midpoint
        self.nodes.append(Node(x-width//2, y-height//2))
        # Top Corner
        self.nodes.append(Node(x         , y-height   ))
        # Top Right Midpoint
        self.nodes.append(Node(x+width//2, y-height//2))
        # Right Corner
        self.nodes.append(Node(x+width   , y          ))
        # Bottom Right Midpoint
        self.nodes.append(Node(x+width//2, y+height//2))
        # Bottom Corner
        self.nodes.append(Node(x         , y+height   ))
        # Bottom Left Midpoint
        self.nodes.append(Node(x-width//2, y+height//2))
        # Left Corner
        self.nodes.append(Node(x-width   , y          ))
        
class Display(Shape):
    '''
    A Paralellagram representing a display or output in a flow chart.
    '''
    def __init__(self, x, y, height, width):
        super().__init__("Rectangle", x, y, height, width)
        self.generate_nodes()
        
    def generate_nodes(self):
        x, y = self.x, self.y
        width, height = self.width//2, self.height//2
        offset = width/3
        self.nodes = []
        
        # Top Left Corner
        self.nodes.append(Node(x-width         , y-height))
        # top Midpoint
        self.nodes.append(Node(x-offset/2      , y-height))
        # Top Right Corner
        self.nodes.append(Node(x+width-offset  , y-height))
        # Right Midpoint
        self.nodes.append(Node(x+width-offset/2, y       ))
        # Bottom Right Corner
        self.nodes.append(Node(x+width          , y+height))
        # Bottom Midpoint
        self.nodes.append(Node(x+offset/2       , y+height))
        # Bottom Left Corner
        self.nodes.append(Node(x-width+offset   , y+height))
        # Left Midbpoint
        self.nodes.append(Node(x-width+offset/2 , y       ))
        
        
