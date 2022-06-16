import math
import random

##############################################################
# ########### ADD YOUR DTMP INSTANCE HERE ####################
##############################################################

# Example 1
# num_cars = 10
# dest_dict = {1: [1, 8], 2: [2, 9], 3: [3, 7], 4: [4, 6], 5: [5, 10]}

# Example 2
# num_cars = 4
# dest_dict = {1: [1, 3], 2: [2], 3: [4]}

# Sanity check
# dest_dict = {i: [i] for i in range(1, num_cars +1)}

# Home-grown example
# num_cars = 10
# dest_dict = {1: [1, 10], 2: [2, 9], 3: [3, 8], 4: [4, 7], 5: [5, 6]}

# tried to break it example
num_cars = 100
car_dest = [random.randint(1,6) for car in range(num_cars)]
dest_dict = {j : [] for j in range(1, 7)}
for car in range(num_cars):
    dest_dict[car_dest[car]].append(car+1)

##############################################################
# ########### DO NOT TOUCH BELOW #############################
##############################################################

num_dest = len(dest_dict)

# The following class requires O(n^2k) time in theory.
# I was lazy and it will take O(n^2kt).
# Since each node of the graph has at most t+1 exiting arcs,
# the space needed to store the graph is O(nkt).


class GRAPH:
    def __init__(self, num_cars, num_dest, dest_dict, des_rail):
        # define vertex set
        # a node for each position in the sequence sigma(n,k)
        # and two extra nodes 0 and nk+1
        self.V = V = [i for i in range(num_cars*des_rail + 2)]

        # define arc set as an adjaceny matrix
        # E[i][j] =\= 0 iff ij is an arc
        # E[i][j] == x =/= 0 iff ij is coloured x
        self.E = E = [[0 for i in range(len(V))] for j in range(len(V))]

        # define sigmas(n, k)
        self.sigma = sigma = [i+1 for i in range(num_cars)]*des_rail
        # sigma = [1, 2, ..., num_cars, ...,  1, 2, ..., num_cars]
        # print("sigmas", sigma)

        # testing understanding from Example 1 (Continued)
        # R = [1,8,9,12,14,16,17,23,25,30]
        # output = []
        # for index in R:
        #     output.append(sigma[index-1])
        # print(output)
        # # output = [1, 8, 9, 2, 4, 6, 7, 3, 5, 10]

        # the following loop constructs the arc arc set of the graph
        # the arc (i, ell), where ell =/= nk+1 is added and coloured
        # j + 1 (j in the paper) iff ell is the minimum ell such that
        # D(j+1) (D(j) in the paper) is a subset of [i+1, ell]
        # if no such ell =/= nk+1 exists then the arc (i, nk+1) is added

        # this first loop constructs E^ in the paper
        for i in range(num_cars*des_rail):
            # define destination membership list
            # note that Algorithm 1 iterates for j = 1 to t
            # and here we iterate for j = 0 to t-1
            s = [0 for j in range(num_dest)]
            # note that Algorithm 1 iterates for h = i+1 to min{i+n, nk}
            for h in range(i + 1, min(i + num_cars, num_cars*des_rail) + 1):

                # deterimine which destination list sigma(n,k)[h] is in
                for j in range(num_dest):

                    # checking the destination of vertex h
                    # input j+1 since the destinations are 1 to num_dest
                    # input h-1 since python index starts at 0 not 1
                    if sigma[h-1] in dest_dict[j+1]:

                        # print("car: ", sigma[h-1], " has dest.: ", j+1)
                        # break the loop if dest. found
                        break

                # input j not j+1 since s is indexed from 0 to num_dest-1
                s[j] = s[j] + 1

                # when the |D(j+1)|th occurence of D(j+1) is encountered in
                # pos. h, then the arc (i,h) of colour j+1 is added to
                # the arc set.
                if s[j] == len(dest_dict[j+1]):
                    E[i][h] = j + 1

        # this adds the arcs from the vertex 1, ..., nk to nk+1
        # this is denoted by E_{nk+1} in the paper
        for i in range(1, num_cars*des_rail+1):
            E[i][num_cars*des_rail+1] = num_dest + 1

# This function is the dynamic programming part of the problem.
# Given an instance of DTMP, the existence of a N_{t+1}-rainbow path in
# the graph G (def by class above), is solved via inclusion-exclusion.
#
# If U is the set of all paths in G from node 0 to node nk+1 w/ t+1 arcs
# and P_j (where j = 1, ..., t) is the subset of paths of U that contain
# at least one arc of the colour j, by inclusin-exclusion, the intersection
# P_1 \cap ... \cap P_t, is  the set of all the N_{t+1}-rainbow paths from 0
# to nk+1 (note that all vertex have the same coloured arc to the vertex nk+1,
# therefore it suffices to consider P_1, ..., P_t and not include P_{t+1})
# and is calculated by
#
# X = sum_{T \subseteq N_t} (-1)^{|T|}*(# paths in U w/ no arc w/ colour T)

# The following dynamic programing routine requires O(nkt^2) time in theory,
# I was lazy and mine runs in O((nk)^2t) time.
# It also requires O(nk) space.


def DYN_PROG(graph, T, num_cars, num_dest, des_rail):
    # N[i][h] in the below list corresonds with the number of paths of
    # length h from node i to node nk+1 whose arcs have colors N_t\T.
    NT = [[0 for i in range(num_dest + 2)] for j in range(num_cars*des_rail + 1)]

    # All nodes have an arc to node nk+1 coloured t+1, therefore we can use the
    # base conditino N[i][1] = 1.
    for i in range(num_cars*des_rail+1):
        NT[i][1] = 1

    # The recursion is computed similar to Dijkstras Algorithm.
    # Give some fixed node i \in [nk] and some distance 2 <= ell <= t+1,
    # the number of paths of length ell from node i to node nk+1 whose
    # arcs have colours in N_t\T (denoted here by NT[i][ell]) is given by
    #
    # NT[i][ell] = sum NT[h][ell-1]
    #
    # where the sum is over all arcs (i,h) from node i to node h which
    # are not coloured by an element of T.
    #
    # Loop over the possible distances to compute.
    # Recall the initial condition that NT[i][1] = 1 for all i \in [nk].
    for ell in range(2, num_dest + 2):

        # Loop over nodes i \in [nk] whom we would like to compute
        # the number of paths of length ell to nk+1.
        for i in range(num_cars*des_rail + 1):

            # Consider all arcs with vertex i as tail and some vertex h
            # other than nk+1
            for h in range(len(graph.V)-1):

                # does the arc exist and is it the right colour?
                if graph.E[i][h] not in T:

                    # sum it via the recursion
                    NT[i][ell] += NT[h][ell-1]

    # Output the # of paths from node 0 to node nk+1 with t+1 arcs of
    # colours in N_t\T
    return NT[0][num_dest+1]


def DTMP(G, num_cars, num_dest, des_rail):
    # generate all possible subset of [t]
    def generate_all_possible_subsets(localsubset, index):

        # make sure the recursion understands that x is a global variable
        global x

        # if we have found a subset of [t]
        if index == num_dest + 1:
            # send graph and given fixed subset into dynamic program
            NT = DYN_PROG(G, localsubset, num_cars, num_dest, des_rail)
            # apply inclusion and exclusion property of Theorem 2
            x += (-1)**(len(localsubset))*NT
            # backtrack
            return

        # proceed with element corresponding to index included in subset
        localsubset.add(index)
        # proceed to next element
        generate_all_possible_subsets(localsubset, index + 1)

        # proceed with element corresponding to index not included in subset
        localsubset.discard(index)
        # proceed to next element
        generate_all_possible_subsets(localsubset, index + 1)

        # backtrack
        return

    # generate the power set of [t] where t = num_dest
    generate_all_possible_subsets(set([]), 1)


# If DTMP is true, the following script finds all valid solutions
def find_sol_TMP(G, num_cars, num_dest, des_rail, dest_dict):

    def build_rainbow_path(local_path, local_valid_colours, index):
        # if we found a rainbow-path with t+1 verices
        if len(local_path) == num_dest + 2:
            # determine order pi of N_t
            pi = [G.E[local_path[i-1]][local_path[i]] for i in range(1, num_dest + 1)]
            # determine R
            # R = [set([]) for j in range(1, num_dest+1)]
            R_union = set([])
            for j in range(1, num_dest + 1):
                for r in range(local_path[j-1]+1, local_path[j]+1):
                    if G.sigma[r-1] in dest_dict[pi[j-1]]:
                        # R[j-1].add(r)
                        R_union.add(r)
            R_union = sorted(R_union)
            # determine total ordering on N_t
            sigma_R = [G.sigma[j-1] for j in R_union]
            # determine which track each car goes to
            car_dir = [0 for car in range(num_cars)]
            for rail in range(1, des_rail + 1):
                interval = set([i for i in range(num_cars*(rail-1)+1, num_cars*rail + 1)])
                for car in set(R_union).intersection(interval):
                    car_dir[G.sigma[car-1]-1] = rail

            print("-----Solution-----")
            print("N_{}-rainbow path formed by nodes: {}.".format(num_dest+1, local_path))
            # print("Order of N_{} is {}".format(num_dest, pi))
            # print("R = {}.".format(R_union))
            print("Final TM order is {}".format(sigma_R))
            print("Cars [1, ..., {}] go to rails {}".format(num_cars, car_dir))
            print("")
            # backtrack
            return 0
        # consider vertices of higher order than current index
        # no need to consider the last vertex since it is the termination
        # vertex in the path
        for i in range(index + 1, len(G.V)):
            # is the arc (index, i) a colour not yet seen in local_path
            if G.E[index][i] in local_valid_colours:
                # proceed with the arc (index, i) included in the path
                local_path.append(i)
                # remove colour of the arc (index, i)
                local_valid_colours.remove(G.E[index][i])
                # proceed to next element
                build_rainbow_path(local_path, local_valid_colours, i)

                # proceed with the arc (index, i) not included in local_path
                local_path.pop()
                local_valid_colours.add(G.E[index][i])

        # backtrack
        return
    # start the path at the node 0
    # valid colours are (1, 2, ..., num_dest + 1)
    build_rainbow_path([0], set([col + 1 for col in range(num_dest + 1)]), 0)


# num_cars = n
# num_dest = t
# dest_dict = D
# des_rail = k

print("Instance of DTMP defined by:")
print("Number of cars n =", num_cars)
print("Number of destionations t =", num_dest)
print("List of cars/destionation D =", dest_dict)
print("")

for des_rail in range(1, math.ceil(num_cars/4 + 1/2)+1):
    # number of t + 1 (num_dest + 1) rainbow paths in the graph G(n,t,D,k),
    # i.e. G(num_cars, num_dest, dest_dict, des_rail), associated to a
    # DTMP instance
    x = 0

    # construct the graph
    G = GRAPH(num_cars, num_dest, dest_dict, des_rail)

    # determine whether or not the DTMP can be done with k rails.
    DTMP(G, num_cars, num_dest, des_rail)

    # interpret results
    if x == 0:
        print("{} rails failed.".format(des_rail))
    else:
        print("{} rails succeeded.".format(des_rail))
        print("")
        find_sol_TMP(G, num_cars, num_dest, des_rail, dest_dict)
        break


