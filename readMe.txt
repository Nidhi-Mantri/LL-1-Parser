Requirements :-  "sys" library
	        :- "collections" library
	        :- "prettytable" library

1.   Input should be given in the exact manner as in the input file.
2.  There must be a space before and after '|', ':', '->'.
3.   Epsilon is denoted by '#'
4.   Proper error handling -> no two same variables, terminals.
5.   All the variables used in productions and in defined in the main variable list must be same.
6.   Single start variable. Name of any variable and any terminal should be of length 1(i.e. single character).
7.   Any grammar that contains epsilon even after the process of removal of epsilon, is not allowed.
	(Ex: - S -> AB | #,  A -> 0A | #, B -> 1B | #) -> this grammar is not allowed.
8.    If there is any violations of above conditions, then it gives the corresponding error in the output file and program will terminate.
9.   If there is indirect recursion like :-
	S -> AB | a
	A -> Sa | a
then the code first remove the indirect recursion and then apply lemma 4.4 to further remove left recursions.     
10.    Output is in the output file, there is nothing to be displayed on console. 
Output file for left recursion is Recursion_removed.txt

Left_Rec.py : - To remove left recursion from the code
Input file is : - input.txt
Output file is : -Recursion_removed.txt

Left_Factoring.py : - 
Input file is : - Recursion_removed.txt
output file is : - Left_factoring_removed.txt

First_Follow.py : - 
Input file is : - Left_factoring_removed.txt
Output file is : - Output.txt, LMD_string.txt
This Output.txt produces both first and follow set and parsing table as well.
Parsing table is printed in the form of dictionary.
example 1 :- 
[E]
-------------------
	[a] -> [E -> a]

it means, in the table :-
row of 'E' and column of 'a' contains the production 'E -> a' 
example 2 : -
[E]
------------------------
	[a] -> [E -> a | aB]
	
it means row of 'E' and column of 'a' contains two productions 'E -> a' and 'E -> aB'

LMD_string.txt : - 
   - produces the left most derivative tree for the string given if it will be completely parsed then output is 'Accepted' , otherwise it will be 'Not Accepted'.
