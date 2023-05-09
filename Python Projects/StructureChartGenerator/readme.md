# Overview
This module convert a python file with stub functions into a structure chart image. The python stub functions should follow the following template.
  def function_name(parameter1, parameter2, etc):
    '''function_description'''
    # Dependencies
    dependencies
    # Return value
    return_value = return_type
    return return_value
[Software Demo Video](Pending Demonstration)

# Development Environment
This module requires the user to have an IDE with Python installed as well as the Python Pillow library. 
To learn how to install python see https://www.python.org/downloads/
To learn how to install Python Pillow see https://pillow.readthedocs.io/en/stable/installation.html

If you are using Visual studio code for your IDE, you can also add this user defined code snippet to help structure the stub functions correctly.
For help learning to create a user defined code snippet, see https://code.visualstudio.com/docs/editor/userdefinedsnippets#_create-your-own-snippets
  {
  "stub function": {
      "prefix": "stub",
      "body": [
        "def ${function_name}(${parameters}):",
        "\t'''${function_description}'''",
        "\t# Dependencies",
        "\t${dependencies}",
        "\t# Return value",
        "\t${return_value} = ${return_type}",
        "\treturn ${return_value}",
        "",
        ""
      ],
      "description": "drafts a python stub function"
      }
    }
# Useful Websites
  While writting this module I used the follwoing resources:
  - [w3schools](https://www.w3schools.com/python/)
    - I used w3schools primarily for python syntax help.
  - [geeksforgeeks](www.geeksforgeeks.org)
    - Geeks for Geeks had many helpful descriptions of how to use the PIL library
    - https://www.geeksforgeeks.org/python-pil-imagedraw-draw-multiline_text/
    - https://www.geeksforgeeks.org/python-pil-imagedraw-draw-line/
    - https://www.geeksforgeeks.org/python-pil-imagedraw-draw-polygon-method/
  - [stackoverflow](www.stackoverflow.com)
    - I found useful code for this project in the following stackoverflow threads 
    - https://stackoverflow.com/questions/245447/how-do-i-draw-text-at-an-angle-using-pythons-pil
    - https://stackoverflow.com/questions/9870876/getbbox-method-from-python-image-library-pil-not-working

# Future Work

The following issues still require some work
- FunctionOvals are spread out too much. Rows with fewer functions should be centered more tightly.
- I would like to add intelligent placment of the ovals. Right now the ovals just fill in from left to right without regard for the functions that call them.
- I would like to add functionality to convert_py_to_json that lets it parse a fully written python file and create a structure chart.
- I would like to add data flow objects as well as a function that can parse a python file into a data flow diagram.


