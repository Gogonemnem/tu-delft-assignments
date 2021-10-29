# Breaksum
Welcome to breaksum. Breaksum is a UI based application for to make work or study from home a more healty and pleasant experience. Below you can find the general structure of the application and repository structure. 

## Repository structure
The breaksum application can be used by running project\main\main.py. All features and functions are directly or indirectly called by main.py. All other folders contain classes and definitions to create the total application. The 'gui' folder contains all classes that define the interface of the application. All buttons, labels, widgets and other elements are defined and visualised in the classes in this folder. The functions that preform calculations or file adjustments are grouped in 3 seperate repositories 'agenda', 'randomizer' and 'task list'. The final folder 'test' contain as the name suggest the test to check if all classes are working properly. There are test for all classes except the UI bases classes.

## Application structure
The breaksum application has two main parts, the main window and a pop-up window. The main window is directly opened when running the code (main.py). The main window has three tabs. 'home', 'file' and 'database'. The home tab is the default tab and contains most of the relevant information and the widgets the user can interact with. The settings tab allows the user to adjust some standard values and the database shows all tasks that are added to the database. In the home tab, the user can interact with the tasks for that day (to do list, upper left), add task to database or agenda (widget, lower left) and the agenda (right). The information button in the programbar allows the user to get extra information. This is done by clicking on the information button and then on the part that needs some explanation.

We hope you enjoy our application.

greeting from the Breaksum team,
```
Betsie
Cristian
Gonem
Janine
Nils
```
