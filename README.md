# CeLang
Simple programming language written in Python for easy Logical Circuit Simulation.

## Table Of Contents
* [Introduction](#introduction)
* [Technologies](#technologies)
* [Usage](#usage)
* [Future](#future)

## Introduction
CeLang stands for Certainty Language and it's being built to work with a logic circuit
simulation software I'm working on. It was built using Python and its main purpose is
to make the process of simulating a logic circuit in programming easier.

## Technologies
CeLang was built using Python 3.12.2 and Sly, a python module made specifically for
the purpose of writing a programming language.

## Usage
### Installation
As stated above, this python program requires the Python and the module Sly.
- To install Python on your system, follow the Python Documentation
- To install Sly on your system, simply run the command on your Terminal:
```
pip install sly
```
Once both Python and Sly are installed, simply run the file "CertaintyLang.py" with
the Python IDLE to start using CeLang.

### Operations
CeLang currently supports the following operations:

- Addition (+)
- Subtraction (-)
- Multiplication (*)
- Division (/)
- Exponentiation (^)

Usage of the above operations is seen below:
```
CeLang > 1+2
3
CeLang > 6-2
4
CeLang > 5*2
10
CeLang > 9/3
3
CeLang > 2^3
8
```

### Comparisons
CeLang currently supports the following comparison operations, to use in IF statements
and WHILE loops:
- Equal (==)
- Less Than (<)
- Less Than Or Equal To (<=)
- More Than (>)
- More Than Or Equal To (>=)

### Pre-Made Functions
- PRINT x: Prints the value of x
```
CeLang > PRINT (1+35)
36
```
- BIN x: Returns the value of x in Binary Form as a String
```
CeLang > BIN 5
101
```

### Command Seperation
The user should use a semicolon (;) to seperate commands in one line, as seen below.
```
CeLang > PRINT 2 ; PRINT (1+2)
```

### Variables
This language currently supports 2 variable types, with more coming in future updates:
- Integers
- Strings
Declaring an Integer or a String is simple:
```
CeLang > i = 2
CeLang > j = "HELLO"
CeLang > i
2
CeLang > j
"HELLO"
```
When dealing with Integer Variables, the following operations are also available:
- "++", which adds 1 to the variable's value
- "+= [number]", which adds [number] to the variable's value

### IF And IF-ELSE Statements
To form an if-else statement:
```
CeLang > IF 2<1 THEN {PRINT 2} ELSE {PRINT 1}
1
```
To form a simple if statement:
```
CeLang > IF 2>1 THEN {PRINT 5}
5
```

### FOR Loops
To form a FOR loop:
```
CeLang > FOR i = 0 TO 10 {PRINT i}
0
1
2
3
4
5
6
7
8
9
```
It is apparent that in the above example i begins at the value 0 and stops at the value 9 (10 - 1).

### WHILE Loops
To form a WHILE loop:
```
CeLang > WHILE i < 6 DO {PRINT i ; i++}
2
3
4
5
```
If the WHILE loop passes 200 iterations, it will stop automatically.

### Functions
To form a Function:
```
CeLang > FUN hi -> {PRINT 2}
```
The statements are put between two curly brackets, and "hi" is the name of the function.

To call a Function:
```
CeLang > hi;
2
```

### Logic Operations:
CeLang currently supports all 2-input Gates:
- x AND y
- x OR y
- x NOT
- x NAND y
- x NOR y
- x XOR y
- x XNOR y

where x and y are Integer Variables, Integer Constants or Integer Expressions.

### Integrated Circuits:
We have added the functionality of the following ICs:

- 2x1 Multiplexer
- 4x1 Multiplexer
- Inverter
- Binary Adder
- Binary Subtractor

Below are usage examples:
```
CeLang > 1, 0 MUX21 0
1
CeLang > 1, 0, 1, 0 MUX4X1 1, 0
1
CeLang > 100 BINVERTER
11
CeLang > 11 BINADDER 10
101
CeLang > 110 BINSUBTRACTOR 10
100
```

### Executing Files
Running a .txt File is easy in CeLang:
```
CeLang > FILEOPEN "[path_to_file]"
```
Or through the Terminal / Command Prompt:
```
python CertaintyLang.py "[path_to_file]"
```
An example of a .txt File for CeLang is:
```
PRINT "HELLO, WORLD!"
FUN TEST -> {I = 1; Y = I * 4; PRINT Y}
TEST;
```

## Future
Future updates coming soon with:
- More Pre-Made Functions
- Logic Operations with more inputs
- More complicated logic gates with integrated circuits
- Bug fixes




