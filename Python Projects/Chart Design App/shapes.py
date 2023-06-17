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
    def __init__(self, shape_type, x, y, height, width):
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.label = ""
        self.generate_nodes()

    def contains_point(self, x, y):
        x_in_range = self.x-self.width//2 <= x and x <= self.x + self.width//2
        y_in_range = self.y-self.height//2 <= y and y <= self.y + self.height//2
        return x_in_range and y_in_range
    
    def draw(self, canvas:tk.Canvas, active:bool, smooth=False):
        points = []
        if active: self.generate_nodes()
        for node in self.nodes:
            points.append(node.x)
            points.append(node.y)
        if not active:
            canvas.create_polygon(
                points,
                outline = STROKE_COLOR, width=STROKE_WIDTH,
                fill=FILL_COLOR, smooth=smooth
            )
        else:
            canvas.create_polygon(
                points,
                outline = SELECTED_STROKE, width=STROKE_WIDTH,
                fill=FILL_COLOR, smooth=smooth
                )   
            for node in self.nodes:
                node.draw(canvas)
                
        self.draw_text(canvas)
    
    def change_label(self, new_text):
        self.label = new_text
        
    def add_to_label(self, text_to_add):
        self.label += text_to_add
    
    def backspace(self):
        self.label = self.label[:-1]
        
    def draw_text(self, canvas):
        canvas.create_text(self.x, self.y, text=self.label, anchor="center" )
    
    def start_mod(self, x, y):
        self.old_x = self.x
        self.old_y = self.y
        self.old_text = self.label
        self.mod_x = x
        self.mod_y = y

    def move(self, x, y):
        self.x = self.old_x + (x - self.mod_x)
        self.y = self.old_y + (y - self.mod_y)
        
    def generate_nodes(self):
        x, y = self.x, self.y
        width, height = self.width//2, self.height//2
        self.nodes = []
        
        self.nodes.append(Node(x-width, y-height))
        self.nodes.append(Node(x      , y-height))
        self.nodes.append(Node(x+width, y-height))
        self.nodes.append(Node(x+width, y       ))
        self.nodes.append(Node(x+width, y+height))
        self.nodes.append(Node(x      , y+height))
        self.nodes.append(Node(x-width, y+height))
        self.nodes.append(Node(x-width, y       ))

class Rectangle(Shape):
    def __init__(self, x, y, height, width):
        super().__init__("Rectangle", x, y, height, width)
        self.generate_nodes()

class Circle(Shape):
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

class RoundedRectangle(Shape):
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
        
class Diamond(Shape):
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
        
        self.nodes.append(Node(x-width//2, y-height//2))
        self.nodes.append(Node(x         , y-height   ))
        self.nodes.append(Node(x+width//2, y-height//2))
        self.nodes.append(Node(x+width   , y          ))
        self.nodes.append(Node(x+width//2, y+height//2))
        self.nodes.append(Node(x         , y+height   ))
        self.nodes.append(Node(x-width//2, y+height//2))
        self.nodes.append(Node(x-width   , y          ))
        