import tkinter as tk
from shapes import *

class Chart(tk.Canvas):
    '''
    A Chart is a tk.Canvas that you can draw shapes on
    ''' 
    def __init__(self, root, bg="white", width=700, height=400) -> None:
        super().__init__(root, bg=bg, width=width, height=height)
        # I plan to add children to the chart class (such as flow chart or 
        # structure chart). For now, this feature is just a stub structure 
        # pending construction.
    
class ShapeMenu(tk.Frame):
    '''
    ShapeMenu definies a menue filled with buttons for creating shapes 
    within a chart.
    '''
    def __init__(self, root, width=300, height=400) -> None:
        super().__init__(root, width=width, height=height)
        # This class does not have any special proerties yet.
        # Once the app is able to display multiple chart types
        # this class will be used to differentiate the shape
        # options available for each type of chart. 

class App:
    '''
    This class will define the functionality of the app as a while, including 
    user input, saving and loading files, and creating new charts, shapes, and 
    projects.
    '''
    def __init__(self):
        
        #  Create the window
        self.root = tk.Tk()
        self.root.title("Chart App")

        # Eventually shapes will be moved to the Chart class, but for now, I 
        # put them here to simplify the scope of this project. My next step 
        # will be to enable the app to save multiple charts and tab between 
        # them. Once I've done that, the shapes will need to be saved, edited, 
        # drawn, and loaded from the chart app.
        self.shapes = []
        self.selected_shape = None

        # This is the menue from which you can create new shapes on the active 
        # Chart
        self.menu_panel = ShapeMenu(self.root, width=200, height=200)
        self.menu_panel.grid(row=0, column=0)

        # This is the active chart. Eventually, new instances of the app will 
        # not have a chart yet, But since the chart selection and 
        # differentiation features aren't ready yet, this is the simplest way 
        # to begin and test the app features.
        self.charts = []
        self.view_panel = Chart(self.root, bg="white", width=700, height=400)
        self.view_panel.grid(row=0, column=1, rowspan=2, sticky="nsew")
        self.active_chart = self.view_panel
        self.charts.append(self.view_panel)
        # This is a panel that displays the properties of the active shape 
        # when a shape is selected.
        self.edit_panel = PropertyPanel(
                                        self.root, self.draw_shapes, 
                                        width=200, height=200, row=1, 
                                        col=0
                                       )

        # These buttons will eventually be in the ShapeMenu class but I need to 
        # figure out how to create the shapes inside a Chart object using a 
        # button inside a different class.
        terminator_button = tk.Button(
                                      self.menu_panel, text="Terminator", 
                                      command=self.add_terminator
                                     )
        terminator_button.pack()

        process_button = tk.Button(
                                    self.menu_panel, text="Process", 
                                   command=self.add_process
                                  )
        process_button.pack()

        decision_button = tk.Button(
                                   self.menu_panel, text="Decision", 
                                   command=self.add_decision
                                  )
        decision_button.pack()
        
        flow_node_button = tk.Button(
                                    self.menu_panel, text="Flow Node", 
                                  command=self.add_flow_node
                                 )
        flow_node_button.pack()
        
        display_button = tk.Button(
                                    self.menu_panel, text="Display", 
                                  command=self.add_display
                                 )
        display_button.pack()
        
        self._build_menus()

        self.view_panel.bind("<Button-1>", self.select_shape)
        self.view_panel.bind("<B1-Motion>", self.move_shape)

    def add_process(self):
        '''
        Adds a process shape to the chart
        '''
        # Eventully I hope to move thi function to either the ShapeMenu class
        # But I need to restructure the functions so that they add to a 
        # provided Chart object.
        rectangle = Process(50, 50, 50, 75)
        index = len(self.shapes)
        rectangle.change_label("Process "+str(index))
        self.shapes.append(rectangle)
        self.draw_shapes()

    def add_flow_node(self):
        '''
        Adds a FlowNode shape to the chart
        '''
        # Eventully I hope to move thi function to either the ShapeMenu class
        # But I need to restructure the functions so that they add to a 
        # provided Chart object.
        flow_node = FlowNode(50, 50, 25, 25)
        index = len(self.shapes)
        flow_node.change_label(str(index))
        self.shapes.append(flow_node)
        self.draw_shapes()

    def add_terminator(self):
        '''
        Adds a terminator Shape to the chart
        '''
        # Eventully I hope to move thi function to either the ShapeMenu class
        # But I need to restructure the functions so that they add to a 
        # provided Chart object.
        terminator = Terminator(50, 50, 25, 50)
        terminator.change_label("Start")
        self.shapes.append(terminator)
        self.draw_shapes()

    def add_decision(self):
        '''
        Adds a Decision Shape to the Chart.
        '''
        # Eventully I hope to move thi function to either the ShapeMenu class
        # But I need to restructure the functions so that they add to a 
        # provided Chart object.
        decision = Decision(50, 50, 50, 75)
        index = len(self.shapes)
        decision.change_label("Decision "+str(index))
        self.shapes.append(decision)
        self.draw_shapes()

    def add_display(self):
        '''
        Adds a Display Shape to the Chart.
        '''
        # Eventully I hope to move thi function to either the ShapeMenu class
        # But I need to restructure the functions so that they add to a 
        # provided Chart object.
        display = Display(50, 50, 50, 75)
        index = len(self.shapes)
        display.change_label("Display "+str(index))
        self.shapes.append(display)
        self.draw_shapes()
    
    def draw_shapes(self):
        '''
        Draws all Shapes in the Chart
        '''
        # Eventually this will be moved to the Chart class.
        self.view_panel.delete("all")
        for shape in self.shapes:
            shape.draw(self.view_panel, self.selected_shape==shape)

    def select_shape(self, event):
        '''
        using a cursor event, finds the shape that the user most likely 
        clicked and saves that shape to self.selected_shape.
        '''
        x, y = event.x, event.y
        selected = None
        for shape in self.shapes:
            if shape.contains_point(x, y) and shape != self.selected_shape:
                selected = shape
                break
            
        if selected:
            self.selected_shape = selected
            selected.start_mod(x, y)
        else:
            if self.selected_shape: 
                # If the chart already has a selected shape, and
                # the mouse click landed inside that shape, we want 
                # to leave that shape selected.but if not, we want to
                # clear our selection.
                if not self.selected_shape.contains_point(x, y):
                    old_selection:Shape = self.selected_shape
                    self.selected_shape = None
                    self.edit_panel.clear()
                    old_selection.draw()
                    
        
        if self.selected_shape:
            self.show_shape_properties()
            self.selected_shape.draw()

    def show_shape_properties(self):
        '''
        Update self.edit_panel based on currentshape selection
        '''
        if self.selected_shape:
            self.edit_panel.display_properties(self.selected_shape)
        else:
            self.edit_panel.clear()

    def move_shape(self, event):
        '''
        Moves a shape based on cursor motion
        '''
        if self.selected_shape!=None:
            shape = self.selected_shape
            x, y, = event.x, event.y
            shape.move(x, y)
            self.draw_shapes()
            self.edit_panel.update_coordinates(shape.x, shape.y)
    
    def _build_menus(self):
        '''
        Builds the menues at the top menu bar of the app.
        '''
        # def set_active_chart(chart_index:int):
        #     '''
        #     Activate a chart from self.charts using the chart index.
        #     '''
        #     # Pending Feature: Chart differentiation
        #     self.active_chart = self.charts[chart_index]
            
        # def add_flow_chart():
        #     pass # Pending Feature
        
        # def add_structure_chart():
        #     pass # Pending Feature
        
        # def add_dfd():
        #     pass # Pending Feature
        
        def add_chart():
            # Pending Feature
            print("Create New Chart in Project.")
            
        
        def new_file():
            '''
            Reset app to initial conditions c
            '''
            print("Create New File")
            pass # Pending Feature
        
        def open_file():
            print("Open Existing File")
            pass # Pending Feature
        
        # def import_chart():
        #     pass # Pending Feature
        
        # def export_chart():
        #     pass # Pending Feature
        
        # def export_all():
        #     pass # Pending Feature
        
        self.menu_bar = tk.Menu(self.root)
        self.file_menu:tk.Menu = tk.Menu(self.menu_bar, tearoff=0)
        # New chart menu
        self.new_chart_menu:tk.Menu = tk.Menu(self.file_menu, tearoff=0)
        
            # Pending Feature: Chart Differentiation
                # self.new_chart_menu.add_command(label="Flow Chart", command=add_flow_chart)
                # self.new_chart_menu.add_command(label="Structure Chart", command=add_structure_chart)
                # self.new_chart_menu.add_command(label="DFD", command=add_dfd)
        self.new_chart_menu.add_command(label="Chart", command=add_chart)
        self.file_menu.add_cascade(menu=self.new_chart_menu, label="New Chart")
        # File options
        self.file_menu.add_command(label="New File", command=new_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Open File", command=open_file)
            # Pending Features: Save File
                # self.file_menu.add_command(label="Import Chart(s)", command=import_chart)
                # self.file_menu.add_separator()
                # self.file_menu.add_command(label="Export Chart", command=export_chart)
                # self.file_menu.add_command(label="Export All", command=export_all)
                # Add file_menu to menu_bar
        self.menu_bar.add_cascade(menu=self.file_menu, label="File")
        
        
        # Chart Edit Menu
        self.edit_chart = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_chart.add_command(label="AddShape", command=self.add_terminator)
        self.menu_bar.add_cascade(menu=self.edit_chart, label="Edit Chart")
        
        self.root.config(menu=self.menu_bar)

    def run(self):
        '''
        Sun main loop.
        '''
        self.root.mainloop()
            
