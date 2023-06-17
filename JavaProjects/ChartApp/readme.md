# Overview

This is my first time working In Java. I am trying to build a chart editor that will allow the user to create and export design charts (such as flow charts, structure charts, and DFDs) In this itteration, I have created demos of the flow chart objects, but there is not currently a way for the user to interact with the flow chart objects without writing code.

This project is written using Java language, with the javaFX library. The project is built using gradle.

This is my first forray into creating desktop applications. I have often wanted to create applications that run on desktop without neededing a coding language or IDE installed, but my previous coding work has mostly been in Python and Javascript which are not capable of creating independent applications. I started with the chart design concept because I am a software engineering student and I want to be able to quickly and easilly create design visuals without relying on pristine handwriting and ideal lighting and camera work to ensure that my teacher or team can read the visual.

Since the code does not yet interface with the user, rather than my normal demosntration video, I will include a screenshot of the window the code would output.

![image](https://github.com/DanielSaunders-SoftwarePortfolio/Public-Portfolio/assets/131573288/03baa456-a7a7-4b6d-9189-ab2b0be0868d)

# Development Environment

This project was built in Visual Studio code using the gradle extension and requiring the javaFX library.

# Useful Websites
The following sites contained useful resources which contributed to my code in a meaningful way.

- [openfx](https://github.com/openjfx/samples/blob/master/IDE/VSCode/Modular/Gradle/hellofx/src/main/java/org/openjfx/MainApp.java)
  - This was the only resource I found that accurately and completely explained how to create a project using javaFX. I downloaded the modular gradle jfx template and followed the istructions in the readme.md in the Gradle directory.
- [Asteroids Game Tutorial](https://java-programming.mooc.fi/part-14/3-larger-application-asteroids)
  - This tutorial gave me a good feel for the Data types in JFX and how they would be used in my applicaiton.

# Future Work
The following features are planned for a futue version of the app
- Allow user to move the ChartObjectst.
- Create arrows to connect ChartObjectst
- Allow user to add nodes to the arrows
- Create the following ChartObjects
  - StructureFunction
  - DataProcessor
  - DataStore
  - DataInteractor
