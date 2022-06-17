This is an implementation of the algorithm in https://www.sciencedirect.com/science/article/pii/S0166218X16304504. At the top of the file you can input your DTMP instance. Running the files determines the minimum number of rails and produces (via a backtrack) all possible solutions.

The basic idea of the problem is as follows. You have train cars, labelled 1 through n, on a train track. Each train car has a desired destination. The question is: How many additional tracks do you need to split from the main track to organize the cars such that when you join them back together again onto one track the train is partitioned into cars by their desired destination?

The solution involves

1. Constructing a digraph G associated with the instance of DTMP

2. Find a bijection between solutions to TMP and rainbow paths with certain characteristics in G

3. Determining the number of such rainbow paths via inclusion-exclusion (the dynamic programming element)

4. Report 'yes' if the number of such rainbow paths is non-zero and 'no' otherwise.

The class GRAPH defines the associated digraph. The function DYN_PROG defines the dynamic programming portion of the solution. The function DTMP uses inclusion-exclusion to determine 'yes' or 'no' to the instance of DTMP.

When using the script, you can define your instance of DTMP by inputting the following on lines 19 and 20:

- num_cars = (the number of cars in the problem)

- des_dict = {1: [cars that go to destination 1], 2: [cars that go to destination 2], ..., t: [cars that go to destination t]}

When run, the script will report the minimum number of rails needed for the given instance of DTMP. A backtracking algorithm is then used to find valid solutions (once one is known to exist). In its current state, the script reports all possible assignments of cars to rails with give valid minimum solutions.


