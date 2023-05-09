from math import sin, cos, atan, pi, degrees, radians
import PIL
from PIL import Image as IMG
from PIL.Image import Image
from PIL.ImageColor import getrgb
from PIL.ImageDraw import Draw
from PIL.ImageOps import colorize
import PIL.ImageFont as ImFont

if __name__ == "__main__":
    from Point import Point
elif __name__.split(".")[0] == "Classes":
    from Classes.Point import Point
else:
    from Point import Point

BLACK  = getrgb('black')
WHITE  = getrgb('white')
BLUE   = getrgb('blue')
WIDTH  = 3
LENGTH = 7
TEXT_SIZE = 20
FONT = ImFont.truetype(r'C:\Users\System-Pc\Desktop\arial.ttf', TEXT_SIZE)


def sqrt(value):
    return value**(1/2)

class DataFlowArrow:
    def __init__(self, lable:str, start_point:Point=Point(), end_point:Point=Point()) -> None:
        self._lable = lable
        self._start_point:Point = start_point
        self._end_point:Point   = end_point
    
    def get_lable(self):
        '''Return lable of self'''
        return self._lable
    
    def set_lable(self, new_lable):
        '''Change value of lable'''
        self._lable = new_lable

    def get_end_point(self):
        '''Return end_point of self'''
        return self._end_point
    
    def set_end_point(self, new_end_point):
        '''Change value of end_point'''
        self._end_point = new_end_point
    
    def get_start_point(self):
        '''Return start_point of self'''
        return self._start_point
    
    def set_start_point(self, new_start_point):
        '''Change value of start_point'''
        self._start_point = new_start_point
    
    def get_magnitude(self):
        '''Return magnitude of self'''
        start = self._start_point
        end   = self._end_point
        x_component = end._x - start._x
        y_component = end._y - start._y
        magnitude = (x_component**2 + y_component**2)**(1/2)
        return magnitude
    
    def get_angle(self) -> int:
        '''Return angle of self in radians'''
        if self._start_point == self._end_point:
            raise ValueError
        dx    = self._end_point.get_x() - self._start_point.get_x()
        dy    = self._end_point.get_y() - self._start_point.get_y()
        angle =  atan(dy/dx) * -1 if dx != 0 else (pi/2 if dy > 0 else -1*pi/2)
        if dx <= 0:
            angle += pi
        return angle
    
    def get_degrees(self):
        '''Return angle of self in degrees'''
        return degrees(self.get_angle())
    
    def get_midpoint(self):
        '''Return midpoint of self'''
        start = self._start_point
        end   = self._end_point
        x     = start.get_x() + (self.get_dx()) / 2
        y     = start.get_y() + (self.get_dy()) / 2
        return Point(x, y)

    def get_dx(self):
        '''Return the change in x of self'''
        return self._end_point.get_x() - self._start_point.get_x()
    
    def get_dy(self):
        '''Return the change in y of self'''
        return self._end_point.get_y() - self._start_point.get_y()

    def get_box(self) -> tuple:
        '''
        returns a tuple of length 4 (x1, y1, x2, y2)
        '''
        x1 = self._start_point.get_x()
        y1 = self._start_point.get_y()
        x2 = self._end_point.get_x()
        y2 = self._end_point.get_y()
        return x1, y1, x2, y2
    
    def __add__(self, point:Point) -> 'DataFlowArrow':
        start = self._start_point + point
        end   = self._end_point  + point
        return DataFlowArrow(self._lable, start, end)

    def __add__(arrow1, arrow2:'DataFlowArrow') -> 'DataFlowArrow':
        end1_start2 = arrow1._end_point - arrow2._start_point
        transitionArrow:DataFlowArrow = arrow2 + end1_start2
        return DataFlowArrow(arrow1._lable, arrow1._start_point, transitionArrow._end_point)
    
    def __add__(self, value:float) -> 'DataFlowArrow':
        dy         = self.get_dy()
        dx         = self.get_dx()
        if dx == 0:
            x = self._end_point.get_x()
            y = self._end_point.get_y() - value
        elif dy == 0:
            x = self._end_point.get_x() + value
            y = self._end_point.get_y()
        else:
            slope      = dy/dx
            pos_dx     = (dx > 0 and value > 0) or (dx < 0 and value < 0)
            pos_dy     = (dy > 0 and value > 0) or (dy < 0 and value < 0)
            x = abs(sqrt(value**2/(1+slope**2))) * (1 if pos_dx else -1)
            y = abs(slope * x) * (1 if pos_dy else -1)
            x = self._end_point.get_x() + x
            y = self._end_point.get_y() + y
        return DataFlowArrow(self._lable, self._start_point, Point(x, y))

    def __radd__(self, point:Point) -> Point:
        start = self._start_point
        end   = self._end_point
        x_component = end._x - start._x
        y_component = end._y - start._y
        self_as_point = Point(x_component, y_component)
        return self_as_point + point

    def __sub__(arrow1, arrow2:'DataFlowArrow') -> 'DataFlowArrow':
        end2_start1 = arrow1._start_point - arrow2._end_point
        transitionArrow:DataFlowArrow = arrow2 + end2_start1
        return DataFlowArrow(arrow1._lable, arrow1._output, transitionArrow._start_point, arrow1._end_point)
    
    def __sub__(self, value:float) -> 'DataFlowArrow':
        return self + (value*-1)

    def __iter__(self):
        yield self._start_point
        yield self._end_point

    def __str__(self) -> str:
        '''Convert arrow to str.'''
        delimiter = " "
        splitter  = "\n"
        return f'({delimiter.join(self._lable.split(splitter))}): {self._start_point} -> {self._end_point}'
    
    def __repr__(self) -> str:
        '''represent arrow as str.'''
        return str(self)

    def invert(self):
        lable = self._lable
        end = self._start_point.copy()
        start   = self._end_point.copy()
        return DataFlowArrow(self._lable, start, end)
    
    def flip_x(self, vertex:Point=None) -> 'DataFlowArrow':
        '''
            Flip the arrow over the vertex provided (or the start point if no 
            vertex is provided) in the y direction
        '''
        # Validate vertex
        if type(vertex) != type(Point()):
            if vertex == None:
                vertex = self._start_point.copy()
            else:
                return -1
        
        # Invert starting point
        dx = vertex.get_x() - self._start_point.get_x()
        x  = vertex.get_x() + dx
        start_point = Point(x, self._start_point.get_y())
        
        # Invert end point 
        dx = vertex.get_x() - self._end_point.get_x()
        x  = vertex.get_x() + dx
        end_point = Point(x, self._end_point.get_y())
        
        # Return results
        return DataFlowArrow(self._lable, start_point, end_point)
    
    def flip_y(self, vertex:Point=None) -> 'DataFlowArrow':
        '''
            Flip the arrow over the vertex provided (or the start point if no 
            vertex is provided) in the y direction
        '''
        # Validate vertex
        if type(vertex) != type(Point()):
            if vertex == None:
                vertex = self._start_point.copy()
            else:
                return -1
        
        # Invert starting point
        dy = vertex.get_y() - self._start_point.get_y()
        y  = vertex.get_y() + dy
        start_point = Point(y, self._start_point.get_x())
        
        # Invert end point 
        dy = vertex.get_y() - self._end_point.get_y()
        y  = vertex.get_y() + dy
        end_point = Point(y, self._end_point.get_y())
        
        # Return results
        return DataFlowArrow(self._lable, start_point, end_point)
    
    def draw(self, image_to_draw_on:Image, color=BLACK, text_only=False, arw_only=False):
        ''' draw a labled arrow on the provided Image object'''

        bg_color     = image_to_draw_on.getpixel((1,1))
        line_end     = int(self.get_magnitude()-LENGTH-WIDTH)+1
        num_lines    = len(self._lable.split("\n"))
        border_mult  = (num_lines + 1)*.75

        # Image height is calculated using the floowing factors
        #    numlines for the height of the text,
        #    border_mult*width. for the height added by the border around the 
        #       text,
        #    LENGTH for the height of the triangle of the arrow,
        #    *2 because the arrow should be drawn at the very center of the 
        #       image to ensure it is rotated correctly.
        text_height  = (num_lines) * (TEXT_SIZE + border_mult*WIDTH) + LENGTH
        img_heigh    = int(text_height + LENGTH) * 2
        img_len      = int(self.get_magnitude())
        # First we draw the arrow from left to right with the text on top in a new image.
        img_size     = img_len if img_len > img_heigh else img_heigh
        arw_img      = IMG.new("L", (img_size, img_size), 0)
        arw_draw     = Draw(arw_img)
        arw_height   = img_size//2
        line_start   = 0 if img_len > img_heigh else (img_heigh - self.get_magnitude())//2
        line_end     = int(line_start + self.get_magnitude()-LENGTH)
        # text_width used to determine if the paste are needs to be 
        # moved to accomodate the text height. See lns 247 and 294
        text_width   = 0
        if num_lines <= 1:
            text_width = int(FONT.getsize(self._lable)[0])+1
        else:
            text_width = int(FONT.getsize_multiline(self._lable)[0])+1
        
        angle        = self.get_angle()
        text_start_width  = (img_size//2) - (text_width//2)
        if angle < (3/2*pi) and angle > (1/2*pi):
           text_start_height =  (img_size//2) - text_height
        else:
            text_start_height =  (img_size//2) + WIDTH + LENGTH
        
        
        # top_crop is the point along the top edge at which arw_img will be 
        # cropped because of the rotation of the image.
        top_crop     = 0
        if sin(angle) != 0:
            top_crop = abs(int(cos(angle) / sin(angle) * arw_height)+1)
            top_crop = top_crop if top_crop < line_end else line_end
        else :
            top_crop = line_end
        # pointer is the three points that make up the triangle at the end of 
        # the arrow.
        pointer1      = (
                        (line_end, arw_height+LENGTH), 
                        (line_end, arw_height-LENGTH), 
                        (line_end+LENGTH, arw_height)
                       )
        pointer2      = (
                        (line_end-2*LENGTH, arw_height+LENGTH), 
                        (line_end-2*LENGTH, arw_height-LENGTH), 
                        (line_end-LENGTH, arw_height)
                        )
        
        txt_img   = IMG.new("L", (img_size, img_size), 255)
        txt_mask  = IMG.new("L", (img_size, img_size))
        
        # Draw the arrow unless text_only is true
        if not text_only: 
            arw_draw.polygon(pointer1, 255)
            arw_draw.polygon(pointer2, 255)
            arw_draw.line((line_start, arw_height, line_end, arw_height), 255, WIDTH)

        if not arw_only:  
            Draw(txt_img).multiline_text((text_start_width, text_start_height), self._lable, 0, FONT, align='center', stroke_width=WIDTH*2, stroke_fill=255)
            Draw(txt_mask).multiline_text((text_start_width, text_start_height), self._lable, 255, FONT, align='center', stroke_width=WIDTH*2, stroke_fill=200)
        
        # Rotate the arw_img
        arw_img        = arw_img.rotate(degrees(angle))
        
        if angle < (3/2*pi) and angle > (1/2*pi):
            txt_img        = txt_img.rotate(degrees(angle+pi))
            txt_mask       = txt_mask.rotate(degrees(angle+pi))
        else: 
            # txt_img        = txt_img.transpose(IMG.TRANSVERSE)
            # txt_img        = txt_img.transpose(IMG.TRANSVERSE)
            txt_img        = txt_img.rotate(degrees(angle))
            txt_mask       = txt_mask.rotate(degrees(angle))
        
        
        min_x          = int(self._start_point.get_x() if self.get_dx() > 0 else self._end_point.get_x())
        min_y          = int(self._start_point.get_y() if self.get_dy() > 0 else self._end_point.get_y())
        arw_radius     = int(self.get_magnitude()//2)
        deg_angle      = degrees(angle)
        angle_comp     = radians((deg_angle+180) % (360))
        trans_x        = int((1-abs(cos(angle_comp)))*arw_radius)
        trans_y        = int((1-abs(sin(angle_comp)))*arw_radius)
        
        min_x         -= trans_x
        min_y         -= trans_y
        
        if img_size > self.get_magnitude():
            trans_x   = int(img_size//2)-arw_radius
            trans_y   = int(img_size//2)-arw_radius
            min_x    -= trans_x
            min_y    -= trans_y


        max_x          = img_size + min_x
        max_y          = img_size + min_y
        box            = (min_x, min_y, max_x, max_y)
        
        color_img  = colorize(arw_img, bg_color, color)

        image_to_draw_on.paste(color_img, mask=arw_img,  box=box)
        image_to_draw_on.paste(txt_img,   mask=txt_mask, box=box)
        
def main():
    # draw grid
    img = IMG.new('RGB', (1000, 1000), WHITE)
    draw = Draw(img)
    # #   Horizontal lines
    # draw.line((0, 100, 1000, 100), BLUE, WIDTH)
    # draw.line((0, 250, 1000, 250), BLUE, WIDTH)
    # draw.line((0, 350, 1000, 350), BLUE, WIDTH)
    # draw.line((0, 500, 1000, 500), BLUE, WIDTH)
    # draw.line((0, 600, 1000, 600), BLUE, WIDTH)
    # draw.line((0, 750, 1000, 750), BLUE, WIDTH)
    # draw.line((0, 850, 1000, 850), BLUE, WIDTH)
    # #   Veritcle lines
    # draw.line((100, 0, 100, 1000), BLUE, WIDTH)
    # draw.line((250, 0, 250, 1000), BLUE, WIDTH)
    # draw.line((350, 0, 350, 1000), BLUE, WIDTH)
    # draw.line((500, 0, 500, 1000), BLUE, WIDTH)
    # draw.line((600, 0, 600, 1000), BLUE, WIDTH)
    # draw.line((750, 0, 750, 1000), BLUE, WIDTH)
    # draw.line((850, 0, 850, 1000), BLUE, WIDTH)
    

    start = Point(100, 100)
    end   = Point(250, 250)
    draw.rectangle((start.to_list(), end.to_list()), BLUE)
    arrow_1 = DataFlowArrow(lable="Test1,\ntest,\ntest\ntest\ntest", start_point=start, end_point=end)
    start = Point(350, 500)
    end   = Point(500, 350)
    draw.rectangle((start.to_list(), end.to_list()), BLUE)
    arrow_2 = DataFlowArrow(lable="Test2", start_point=start, end_point=end)
    start = Point(750, 600)
    end   = Point(600, 750)
    draw.rectangle((start.to_list(), end.to_list()), BLUE)
    arrow_3 = DataFlowArrow(lable="Test3", start_point=start, end_point=end)
    start = Point(850, 850)
    end   = Point(1000, 1000)
    draw.rectangle((start.to_list(), end.to_list()), BLUE)
    arrow_4 = DataFlowArrow(lable="Test4", start_point=start, end_point=end)
    start = Point(175, 600)
    end   = Point(175, 750)
    draw.rectangle((start.to_list(), end.to_list()), BLUE)
    arrow_5 = DataFlowArrow(lable="Test5", start_point=start, end_point=end)
    start = Point(100, 250)
    end   = Point(250, 250)
    draw.rectangle((start.to_list(), end.to_list()), BLUE)
    arrow_6 = DataFlowArrow(lable="Test6", start_point=start, end_point=end)
    arrow_1.draw(img, BLACK)
    arrow_2.draw(img, BLACK)
    arrow_3.draw(img, BLACK)
    arrow_4.draw(img, BLACK)
    arrow_5.draw(img, BLACK)
    arrow_6.draw(img, BLACK)
    img.show()

if __name__ == "__main__":
    main()
