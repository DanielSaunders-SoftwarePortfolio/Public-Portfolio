from json import load as j_load

def convert_py_to_json(file_path):
    '''Open a python file using the provided path and return a json/dict object.'''
    my_py = open(file_path, "r")
    py_lines = my_py.readlines()
    results = {}
    inside_func_def = False
    lines_in_this_func = []
    for line in py_lines:
        if line[0:3] == "def": 
            if not inside_func_def:
                inside_func_def = True
            else:
                my_func = convert_lines_to_func_oval(lines_in_this_func)
                results[my_func.get_name()] = my_func
            lines_in_this_func = [line]
                
        elif inside_func_def:
            lines_in_this_func.append(line)
    my_func = convert_lines_to_func_oval(lines_in_this_func)
    results[my_func.get_name()] = my_func
    return results

def is_valid_line(line):
    '''
    Takes line as str and returns true if the line contains non-whitespace 
    charachters and does not begin with a "#", "=" or 3X"'" in a row.
    '''
    results = True
    results = results and (not "#" in line) # Line is not a comment
    results = results and (not "'''" in line) # line is not a block quote
    results = results and (not "=" in line) # line has no assignment
    results = results and (line.strip().split(" ")[0] != "return") # line is not a return line
    results = results and (len(line.strip()) > 0) # Line is not empty
    
    return results

def convert_lines_to_func_oval(lines:list):
    '''
    Takes a list of strings representing a python function.
    returns a FunctionOval object
    '''
    name, parameters = process_function_definition(lines[0])
    dependencies = []
    i = 1
    description = ""
    
    # Process block quotes in the first line of the 
    # function definition as the funciton description.
    if "'''" in lines[i]:
        if lines[i][-4:-1] == "'''": # Single line block quote
            description = lines[i]
            description = description.strip()[3:-3]
            i += 1
        else: # Multiline block quote
            for i in range(i, len(lines)):
                line = lines[i]
                if "'''" not in line: description += line
                else: 
                    i += 1
                    break

    for i in range(i, len(lines)):
        line = lines[i]
        words = line.strip().split(" ")
        if is_valid_line(line): # not empty, no comments, no assignment, no return.
            dependencies.append(words[0])
        elif "return" in line: # Last line of function
            output = line.strip()
            output = output.replace("return", "")
            output.replace(" ", "")
            if output == "return": output = "" 
    # Construct and return a function oval with these properties.
    return FunctionOval(name, output, parameters, dependencies, description=description)

def process_function_definition(line_str) -> tuple:
    '''
    Split up the first line of a python function into its name and parameters.
    returns (name, parameter)
    '''
    line_list = line_str.split(" ")
    if (line_list[0]=="def"):
        name = line_list[1].split("(")[0]
        line_str = line_str.replace("def ", "")
        line_str = line_str.replace(name, "")
        line_str = line_str.replace("(", "")
        line_str = line_str.replace(")", ",")
        line_str = line_str.replace(" ", "")
        unfiltered_parameters = line_str.split(",")[0:-1]
        parameters = []
        for param in unfiltered_parameters:
            parameters.append(param.split(":")[0])
        return name, parameters
    else:
        return -1

def main():
    file_path = "python_stubs_test_file.py"
    results = convert_py_to_json(file_path)
    print(results)


if __name__ == "__main__":
    from FunctionOval import FunctionOval
    main()
else:
    if __package__:
        from Classes.FunctionOval import FunctionOval
    else:
        from FunctionOval import FunctionOval
