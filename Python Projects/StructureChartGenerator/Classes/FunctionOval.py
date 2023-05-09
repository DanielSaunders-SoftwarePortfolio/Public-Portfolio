from PIL import Image as IMG
from PIL.Image import Image
from PIL.ImageDraw import Draw
import PIL.ImageFont as ImFont
if __name__ == "__main__":
    from Point import Point
    import Arrows as Arr
    from Arrows import BLACK, WHITE
elif __name__.split(".")[0] == "Classes":
    from Classes.Point import Point
    import Classes.Arrows as Arr
    from Classes.Arrows import BLACK, WHITE
else:
    from Point import Point
    import Arrows as Arr
    from Arrows import BLACK, WHITE


TEXT_SIZE = 36
FONT      = ImFont.truetype(r'C:\Users\System-Pc\Desktop\arial.ttf', TEXT_SIZE)
RADIUS    = 10

class FunctionOval:
    def __init__(self, name, output:str="", parameters:list=[], 
                 dependencies:list=[], callers:list=[], description:str="",
                 center:Point=Point()
                ) -> None:
        self._name         = name
        self._parameters   = parameters
        self._output       = output
        self._dependencies = dependencies
        self._callers      = callers
        self._description  = description
        self._center       = center
    
    def get_width(self):
        '''Return length of self'''
        return FONT.getsize(self._name)[0]

    def get_height(self):
        '''Return height of self'''
        return TEXT_SIZE *2

    def get_name(self)->str:
        return self._name
    
    def get_parameters(self):
        '''Return parameters of self'''
        return self._parameters
    
    def get_output(self):
        '''Return output of self'''
        return self._output
    
    def get_dependencies(self):
        '''Return dependencies of self'''
        return self._dependencies
    
    def get_callers(self):
        '''Return callers of self'''
        return self._callers
    
    def get_depth(self):
        '''Return depth of self'''
        return len(self._callers)

    def get_x(self):
        '''Return x of self'''
        return self._center.get_x()

    def get_y(self):
        '''Return y of self'''
        return self._center.get_y()

    def set_x(self, new_x):
        '''Change value of x'''
        self._center.set_x(new_x)
    
    def set_y(self, new_y):
        '''Change value of y'''
        self._center.set_y(new_y)

    def set_name(self, new_name):
        '''Change value of name'''
        self._name = new_name
    
    def set_output(self, new_output):
        '''Change value of output'''
        self._output = new_output

    def set_center(self, new_center):
        '''Change value of center'''
        self._center = new_center

    def get_center(self):
        return self._center.copy()

    def add_parameter(self, new_parameter):
        '''Add another parameter'''
        self._parameters.append(new_parameter)
    
    def add_dependency(self, new_dependency):
        '''Add another dependency'''
        self._dependencies.append(new_dependency)
    
    def add_caller(self, new_caller):
        '''Add another caller'''
        self._callers.append(new_caller)
    
    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        '''
        Return a multiline string representing a stub function with 
        the dependencies, parameters, and return value of this object
        '''
        name = self._name
        parameters = ", ".join(self._parameters)
        dependencies = "\n\t".join(self._dependencies)
        output = self._output
        description = self._description
        results  = f'def {name}({parameters}):\n'
        results += f"\t'''\n\t{description}\n\t'''\n" if description else ""
        results += f"\t# Dependencies\n\t{dependencies}\n" if dependencies else "None"
        results += f"\t# Return value\n\treturn {output}\n\n"
        return results
    
    def __len__(self) -> str:
        return self.get_width()

    def draw(self, image_to_draw_on:Image):
        '''
        Draw FunctionOval as a white oval with black outline and black text 
        for the function name.
        '''
        text_width   = FONT.getsize(self._name)[0] * 1.5
        text_height  = TEXT_SIZE * 2
        min_x        = int(self.get_x() - text_width/2)
        min_y        = int(self.get_y() - text_height/2)
        max_x        = int(self.get_x() + text_width/2)
        max_y        = int(self.get_y() + text_height/2)
        bounding_box = min_x, min_y, max_x, max_y
        draw         = Draw(image_to_draw_on)
        mode = image_to_draw_on.mode
        if mode == "RGB":
            draw.rounded_rectangle(bounding_box, RADIUS, WHITE, BLACK, Arr.WIDTH)
        else:
            draw.rounded_rectangle(bounding_box, RADIUS, 255, 255, Arr.WIDTH)
        
        if image_to_draw_on.mode == "RGB":
            draw.text(self._center.to_list(), self._name, BLACK, FONT, 'mm')
        
        return image_to_draw_on

def main():
    img     = IMG.new("RGB", (1000, 1000), WHITE)
    oval    = FunctionOval("test_1", center=Point(250, 250))
    oval.draw(img)
    img.show()

if __name__ == "__main__":
    main()
