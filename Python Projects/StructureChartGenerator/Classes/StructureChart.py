from PIL import Image as IMG
from PIL.Image import Image
from PIL.ImageDraw import Draw
from math import sin, cos, tan, pi

if __name__ == "__main__":
    from FunctionOval import FunctionOval
    import Arrows as ARR
    from Arrows import DataFlowArrow
    from Arrows import BLACK, WHITE
    from Arrows import Point, sqrt
    from convert_py_to_json import convert_py_to_json as py2json
    from FunctionOval import FunctionOval
elif __name__.split(".")[0] == "Classes":
    from Classes.FunctionOval import FunctionOval
    import Classes.Arrows as ARR
    from Classes.Arrows import DataFlowArrow
    from Classes.Arrows import BLACK, WHITE
    from Classes.Arrows import Point, sqrt
    from Classes.convert_py_to_json import convert_py_to_json as py2json
    from Classes.FunctionOval import FunctionOval
else:
    from FunctionOval import FunctionOval
    import Arrows as ARR
    from Arrows import DataFlowArrow
    from Arrows import BLACK, WHITE
    from Arrows import Point, sqrt
    from convert_py_to_json import convert_py_to_json as py2json
    from FunctionOval import FunctionOval


DFA          = DataFlowArrow
WIDTH_MULT   = 5
HEIGHT_MULT  = 3
ARROW_OFFSET = 15


class StructureChart:
    def __init__(self, file_path) -> None:
        '''function_description'''
        self._functions   = py2json(file_path)
        self._structure   = self.build_structure()
        self.update_function_callers()

    def update_function_callers(self):
        func_i:FunctionOval
        func_j:FunctionOval
        for func_i in self._functions.values():
            for func_j in self._functions.values():
                if func_i in func_j.get_dependencies():
                    func_i.add_caller(func_j)

    def __str__(self) -> str:
        results = ""
        for level in self._structure:
            results += "  |  ".join(func.get_name() for func in level)
            results += '\n\n'
        return results

    def get_width(self) -> int:
        '''function_description'''
        structure_width = max(len(item) for item in self._structure)
        max_oval_width  = max(self._functions[item].get_width() for item in self._functions)
        return int(structure_width * max_oval_width * WIDTH_MULT + 1)
    
    def get_height(self) -> int:
        '''function_description'''
        structure_depth = len(self._structure)
        level_height    = list(self._functions.values())[0].get_height()
        return int(structure_depth * level_height * HEIGHT_MULT)
    
    def get_unit_length(self):
        '''function_description'''
        return
    
    def get_structure(self):
        '''Return structure of self'''
        return self._structure
    
    def build_structure(self):
        '''function_description'''
        def recurs_through_funcitons(hierarchy:list, all_funcitons, current_function=None, depth=1):
            '''
            Using recursion, work through functions to define callers, and assign 
            to structure depth.
            '''

            # When we recurse to a new level, add a level to the heierarchy
            if depth >= len(hierarchy):
                hierarchy.append([])
            if current_function == None:
                current_function:FunctionOval = all_funcitons["main"]
            my_dependencies:list = current_function.get_dependencies()
            if depth == 1: # Set up initial hierarchy
                for dep in my_dependencies:
                    if dep in all_funcitons: 
                        hierarchy[depth].append(all_funcitons[dep])
            for dep in my_dependencies:
                if dep in all_funcitons:
                    subordinates = recurs_through_funcitons(
                                                            hierarchy, 
                                                            all_funcitons, 
                                                            all_funcitons[dep],
                                                            depth+1
                                                           )
                    for sub in subordinates: 
                        if sub in all_funcitons:
                            hierarchy[depth+1].append(all_funcitons[sub])
            return my_dependencies
        
        # Begin recursion with main.
        main     = self._functions['main']
        results  = [[main]] 
        recurs_through_funcitons(results, self._functions)
        
        # Remove any empty levels of the results hiererarchy.
        results        = (level for level in results if len(level)>0)
        results        = list(results)

        # With the structure generated, we can give the functionOval
        # objects their midpoints
        max_cols       = max(len(item) for item in results)
        max_oval_width = max(self._functions[item].get_width() for item in self._functions)
        width          = max_cols * max_oval_width * WIDTH_MULT
        row_height     = results[0][0].get_height() * HEIGHT_MULT
        y              = row_height // 2
        col: FunctionOval
        for row in results:
            num_cols = len(row)
            col_width = width // num_cols
            x         = col_width // 2
            for col in row:
                center = Point(x, y)
                col.set_center(center)
                x        += col_width
            y        += row_height
        return results
    
    def get_callers_of_function(self, func_to_check_for):
        '''function_description'''
        callers = []
        for func_to_look_in in self._functions:
            if func_to_check_for in func_to_look_in["dependencies"]:
                callers.append(func_to_look_in)
        return callers
    
    def get_max_length(self, attr_to_check):
        '''function_description'''
        # Dependencies
        None
        # Return value
        max_attr_length = int
        return max_attr_length
    
    def draw(self) -> Image:
        '''Draw structure chart to image object.'''
        def generate_arrow(oval:FunctionOval, start:Point, end:Point, lable:str, offset1:int=0, offset2:int=0, off_up:int=0):
            '''Create a draw the arrows between function ovals'''
            oval_height = oval.get_height()
            oval_width  = oval.get_width()*1.1
            end_copy    = end.copy()
            start_copy  = start.copy()
            dy = end.get_y() - start.get_y()

            if dy > 0: # Param Values 
                if abs(offset1) > oval_width/2:
                    extra_offset = abs(offset1)-oval_width/2
                    offset1      = oval_width/2 * (-1 if offset1<0 else 1)
                    off_up       = extra_offset if abs(extra_offset)<oval_height else oval_height
                start_copy.set_y(start.get_y() + oval_height//2 - off_up)
                end_copy.set_y(end.get_y() - oval_height//2)
            elif dy < 0: # Return Values 
                if abs(offset2) > oval_width/2:
                    extra_offset = abs(offset2)-oval_width/2
                    offset2      = oval_width/2 * (-1 if offset2<0 else 1)
                    off_up       = extra_offset if abs(extra_offset)<oval_height else oval_height
                start_copy.set_y(start.get_y() - oval_height//2)
                end_copy.set_y(end.get_y() + oval_height//2 - off_up)
            start_copy.set_x(start.get_x() + offset1)
            end_copy.set_x(end.get_x() + offset2)
                

            arrow:DFA = DataFlowArrow(lable, start_copy, end_copy)
            arrow    -= ARR.LENGTH
            return arrow
        

        im_height = self.get_height()
        im_width  = self.get_width()
        # This Image will hold the arrows and the lables of the arrows
        # for the structure chart.
        arr_img   = IMG.new("RGB", (im_width, im_height), WHITE)
        # The Image that holds the Ovals and function names
        oval_img  = IMG.new("RGB", (im_width, im_height), WHITE)
        # This Image is all black and the ovals will be all white
        # This allows the program to know where the ovals are so it
        # Can paste them later without the white background covering
        # up the arrows we already drew.
        oval_mask = IMG.new("L"  , (im_width, im_height))
        structure = self._structure
        arrows    = []
        # Starting from the bottom of the structure, draw each oval and the 
        # arrows between them.
        for level in reversed(structure):
            func:FunctionOval
            for func in level:
                func.draw(oval_img)
                func.draw(oval_mask)
                dependencies = func.get_dependencies()
                dependencies = list(filter((lambda item: item!='None' and len(item)>0), dependencies))
                start:Point  = func.get_center().copy()
                
                # Draw the arrows (without text) between FunctionOvals
                num_arrows   = 0
                for dep in dependencies:
                    dep_func:FunctionOval = self._functions[dep]
                    params      = list(filter((lambda item: item!='None' and len(item)>0), 
                                              dep_func.get_parameters()
                                             )
                                      )
                    has_params  = len(params) > 0
                    has_output  = (dep_func.get_output() != "None" and 
                                   len(dep_func.get_output()) > 0
                                  )
                    if has_params:
                        num_arrows += 1
                    if has_output:
                        num_arrows += 1
                    if not (has_output or has_params):
                        num_arrows += 1
                    num_arrows += 1
                        
                if num_arrows > 1:
                    oval_offset = ARROW_OFFSET 
                    arw_offsets = list((oval_offset*(value-int(num_arrows/2))) for value in range(num_arrows))
                else: 
                    oval_offset = 0
                    arw_offsets = [0]
                    
                this_arrow   = 0
                for dep in dependencies:
                    dep_func:FunctionOval = self._functions[dep]
                    params      = list(filter((lambda item: item!='None' and len(item)>0), 
                                              dep_func.get_parameters()
                                             )
                                      )
                    has_params  = len(params) > 0
                    has_output  = (dep_func.get_output() != "None" and 
                                   len(dep_func.get_output()) > 0
                                  )
                    end:Point   = dep_func.get_center().copy()
                    oval_width  = dep_func.get_width()

                    # Draw parameter arrow.
                    if has_params:
                        arw_offset = arw_offsets[this_arrow]
                        offset_up  = -1*(0 if abs(arw_offset)<oval_width/2 else func.get_height()/2)
                        dep_offset = 0 if not has_params else (oval_offset/-2)
                        
                        lable      = ",\n".join(dep_func.get_parameters())
                        
                        arrows.append(generate_arrow(dep_func, start, end, lable, arw_offset, dep_offset, offset_up))
                        this_arrow += 1
                    
                    # Draw output arrow
                    if has_output:
                        arw_offset = arw_offsets[this_arrow]
                        dep_offset = 0 if not has_params else (oval_offset/2)
                        offset_up  = 0 if abs(arw_offset)<oval_width/2 else func.get_height()/2
                        lable      = dep_func.get_output()
                        arrows.append(generate_arrow(func, end, start, lable, dep_offset, arw_offset, offset_up))
                        this_arrow += 1

                    # If there is neither parameters nor output, just draw a line.
                    if not (has_output or has_params):
                        arw_offset = arw_offsets[this_arrow]
                        draw_image = Draw(arr_img)
                        start.set_x(start.get_x() + arw_offset)
                        start.set_y(start.get_y() - func.get_height()/2)
                        end.set_y(end.get_y() + func.get_height()/2)
                        draw_image.line((start.to_list(), end.to_list()), BLACK, ARR.WIDTH)
                        this_arrow += 1
                    
                    this_arrow += 1 # Add a spacer between arrows of different dependencies.
        arrow:DFA
        for arrow in arrows: # Draw arrows only
            arrow.draw(arr_img, BLACK, arw_only=True)
        for arrow in arrows: # Draw text only
            # Text is draw second to make sure no arrows are drawn over any text
            arrow.draw(arr_img, BLACK, text_only=True)
        
        # Draw FunctionOvals last to ensure that no arrows are drawn over the ovals
        arr_img.paste(oval_img, mask=oval_mask)
        return arr_img

def main():
    # Load structure chart from demo file.
    my_struc_chart = StructureChart("python_stubs_test_file.py")
    img = my_struc_chart.draw()
    img.show()

if __name__ == "__main__":
    main()
