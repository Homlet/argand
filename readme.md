## ![](http://i.imgur.com/MLhXJS4.png) Argand Plotter

 Argand Plotter is a program for drawing Argand Diagrams. The program was
 created by Sam Hubbard, as a project for his A2 computing coursework.

### Structure

 The program object has three members:

    program
    | window
    | diagram
    | preferences

 `diagram` and `window` both have references to the program object. The
 `diagram` object stores the currently loaded diagram including all of
 the current plots. It also handles serialising diagrams to `.arg` files.
 The `window` object is a `QMainWindow` subclass which handles the entire
 GUI. `preferences` is a simple object which stores a few diagram
 unspecific preferences. Currently there is no persistence of preferences
 between instances. 

### Building

 To build the program to an executable, you will need
 [cx_Freeze](http://cx-freeze.sourceforge.net/), a tool for generating
 binaries from Python projects. When it is properly installed, run
 `build_exe.bat` from the root folder of the project.

 To make the installer, you will need
 [Inno Setup](http://www.jrsoftware.org/isinfo.php).
 Run `build_installer.bat` from the root folder.

 Alternatively, you can run `build.bat` to do both of these tasks.

----------

 Written by Sam Hubbard - [samlhub@gmail.com](mailto:samlhub@gmail.com)  
 Argand Plotter is Copyright (C) 2015 Sam Hubbard
