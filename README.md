*Created by: Lidor Azani & Barak Ben Acon*\
*Last Update: 18/06/2023*


This code is exercise 2 in course "Biological Computation" by Hillel Kugler.\
The code have been created using "PyCharm 2021.3.1 (Community Edition)".
You can download directory as a folder to your local machine and run the files.


*PART A:*\
In part A the program computes, for a given "n" which is number of vertices, all unique models of connected directed sub-graphs, which called "motifs".
There are 4 text files with outputs for n=1 to 4, called "motifs_n".
At the end of running part a, the program outputs a graph of running times for different n values. 

Note: Our tests show that for n=4 the program runs for 10-30 seconds.
For n=5, the program runs over 24 hours.


*PART B:*\
In this part, the program gets a value of "n" and a graph from user via file "input.txt".
The program from part A have been modified to find & count all motifs of size n (user input) for the input graph, and output it to a text file "output.txt".