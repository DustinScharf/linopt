# linopt
Solver for linear problems  

![Mathematical expression of a linear problem](problem_eq.svg "Linear Problem")

## Table of contents
1. Installation
2. Input Problems
3. Solve Problems

## Installation
First you need [Python (3.9)](https://www.python.org/downloads/release/python-3913/ "Download Python 3.9")
and [Pip](https://www.python.org/downloads/release/python-3913/ "Download Pip") (should come with Python).

1. Download [linopt](TODO "Download linopt")
2. Extract linopt to a folder / directory of your choice
3. Open a terminal / cmd inside linopt was exacted to
4. Type ``pip install -r requirements.txt``
   1. If this fails, you need to install the packages listed in ``requirements.txt`` manually
5. Type ``python linopt.py version`` to test if the installation was successfull

Now you can run the program with a terminal / cmd from the current linopt folder / directory like shown below.

## Input Problems
Problems are saved in CSV files like shown below
```csv
x       ,   ... ,   x       ,   type    ,   b
c_1     ,   ... ,   c_n     ,   z       ,   max
A_11    ,   ... ,   A_1n    ,   <=      ,   b_1
...     ,       ,   ...     ,           ,   ...
A_11    ,   ... ,   A_1n    ,   <=      ,   b_1
```

An example problem input is
```csv
x,x,type,b
1,3,z,max
6,5,<=,90
4.5,7.5,<=,90
0,1,<=,9
```

Just create a file like ``my_problem.csv`` and enter your own problem.

<hr>

Some other inputs can be handled too
```csv
x,x,type,b
1,3,z,max
20,25,bound,u
0,0,bound,l
-6,-5,>=,-90
-4.5,-7.5,>=,-90
0,-1,>=,-9
```

## Solve Problems
The get a first view type ``python linopt.py test.csv print`` in the terminal and press enter.

Type ``python linopt.py my_problem.csv`` to solve a problem directly.  
Type ``python linopt.py`` to get a tour with some additional settings.  
Type ``python linopt.py my_problem.csv eta`` to use eta basis factorisation.  
Type ``python linopt.py my_problem.csv eta 20`` to additionally set basis factorisation reset number manual.  

Just add ``print`` to any command to print the current iteration and some infos about the current calculation.   
For example type ``python linopt.py my_problem.csv print``

## Class Diagramm
Soon...