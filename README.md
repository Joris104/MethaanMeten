# MethaanMeten
VOP project 3de Bachelor Methaan Meten

This github contains all the code relevant to the MethaneNose project, which aims to be able to continuously (~once per min.) measure methane
concentrations in a simulated cow stomach.

\MethaanMeten contains the Arduino code that runs on the micro-controller
\Data contains all data from previous experiments
\Figuren contains several relevant figures from previous experiments

controller.py is the old communication code between the PC and the Arduino and is deprecated.
It was replaced by MethaneNose.py, which contains code for serial communication & live data plotting.
data_graph.py renders a graph of the selected .csv file.
