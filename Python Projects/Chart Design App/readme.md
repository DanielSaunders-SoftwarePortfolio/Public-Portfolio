# Overview

This app will help the user design a flow chart. The user can insert each different flow chart shape and change the labels positions and dimensions of the shapes in the chart.

I built this app to help create professional looking design documents for my future software projects.

[Software Demo Video](https://youtu.be/kEA8Lkzlq54)

# Development Environment

I wrote the code for this app in Visual Studio Code. The app was written in python using the tkinter library and compiled using the pyinstaller library to export project into an executable file.

# Useful Websites

- [This post](https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners) helped me with drawing rounded rectangles
- [This site](http://url.link.goes.here) helped me with drawing text over my shapes.
I also used resources and experience from these two previous projects in this repository.
- [Structure Chart Generator (Python)](https://github.com/DanielSaunders-SoftwarePortfolio/Public-Portfolio/tree/main/Python%20Projects/StructureChartGenerator)
- [Chart App (Java)](https://github.com/DanielSaunders-SoftwarePortfolio/Public-Portfolio/tree/main/JavaProjects/ChartApp)

# Future Work
- Shapes
  -	Add ability to delete chart shapes
  -	Draw ghost shape in original location while moving
- Charts
  -	Create multiple child classes for chart subtypes
    - Change shape_menu based on chart type
  - Snap Arrow start and end Nodes to shape Nodes
  - Add visible
  -	Be able to edit the nodes of shapes or arrows.
- Apps
  -	Be able to save projects
  -	Be able to load projects
  -	Include the ability to have multiple charts loaded in a single window
    -	Include a menu to select the chart you would like to see and edit.
    -	Move shape storage and modification functions to chart objects instead of app objects.
  -	Add saveable app preferences to customize user experience.
    -	Color themes
    -	Custom Chart templates
  -	Add Controls
    -	Escape during Shape movement replaces shape to its original location
- Arrows
  - Add Arrows to indicate chart flow.
    - Arrows have a beginning node, and an end node.
    - Arrows draw a directed triangle at the end node
    - Arrows may have more nodes between the beginning and end nodes (elbow arrows)
    - Arrows may or may not have a label. (Labels are alwasy drawn updright and never rotated)

