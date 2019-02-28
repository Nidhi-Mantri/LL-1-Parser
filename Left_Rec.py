# Program to implement lemma 4.4 to remove left recursions.
import sys

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = list(letters)

with open("input.txt","r") as myfile:
    V = myfile.readline().split(':')[1].strip(" \n")
    V = V.split(', ')
    T = myfile.readline().split(':')[1].strip(" \n")
    T = T.split(', ')
    S = myfile.readline().split(':')[1].strip(" \n")
    P = myfile.readlines()[1:]
#print "V : %s" %V
#print "T : %s" %T
#print "S : %s" %S
#print "P : %s" %P
for i in V:
    letters.remove(i)
output = open("Recursion_removed.txt", 'w')
# Validity of Variables
for i in V:
    c = V.count(i)
    if c > 1:
        output.write("Error -> Two or more same variables -> Invalid Grammar.")
        sys.exit()

# Validity of Terminals
for i in T:
    c = T.count(i)
    if c > 1:
        output.write("Error -> Two or more same terminals -> Invalid Grammar.")
        sys.exit()

# Validity of Start Variable
s = len(S)
if s > 1:
    output.write("Error -> Start Variable more than one -> Invalid Grammar.")
    sys.exit()

# assign all the productions to the variable in dictionary form  
prodt = {}
for i in xrange(len(P)):
    x = P[i].split(' -> ')
    y = ''.join(x[1].split(' |')).strip('\n')
    y = y.split(' ')
    prodt[x[0]] = y
#print prodt

#print "Productions : -"
# variables used in productions P and in V must be same
for i in V:
    if i not in prodt.keys():
        output.write("Error -> Grammar is not correct\n")
        output.write("Variables used in productions P and defined in V must be same\n")
        print "~~~~~~~~~~~~~~~~~~"
        sys.exit()
    #else:
        # all productions
        #print i," -> ", prodt[i]

# epsilon detection
epsilon = []
for i in V :
    if '#' in prodt[i] :
        prodt[i].remove('#')
        epsilon.append(i)
#print epsilon

# To remove epsilon
while epsilon:
    for i in V:
        for j in prodt[i]:
            if epsilon[0] in j:
                index = j.find(epsilon[0])
                #j = j.replace(epsilon[0], '')
                j = j[:index] + j[index+1:]
                if len(j) == 0:
                    j = '#'
                prodt[i].append(j)
    del epsilon[0]

# if epsilon still exists then exit           
for i in V :
    if '#' in prodt[i] :
        output.write("Error -> Can't proceed further, epsilon always remains there in productions.\n")
        sys.exit()

var = []
ans_var = []
# if indirect recursion exists
for i in V:
    if i == S:
        continue
    for j in prodt[i]:
        if j[0] is S and i not in var:  ###### S in j
            var.append(i)
if var :
    all_v = []
    prodtion = []
    for i in prodt[S]:
        x = i[0]
        if x in V and x not in all_v:
            all_v.append(x)
            prodtion.append(i)
    new_prodt = []
    print prodtion, 
    print all_v
    # putting the productions that variable to make direct recursions
    while prodtion:
        i = prodtion[0]
        k = i[0]
        if i in prodt[S]:
            prodt[S].remove(i)
        for j in prodt[k]:
            y = j + i[1:]
            if y[0] in V and y[0] not in var and y[0] != S:
                prodtion.append(y)
            else:
                new_prodt.append(y)
        del prodtion[0]
        prodt[S] += new_prodt
    for l in new_prodt:
        k = l[0]    
        if k in var and k not in all_v:
            prodt[S].remove(l)
            for j in prodt[k]:
                y = j + l[1:]
                prodt[S].append(y)
            var.remove(k)
#print prodt
## Lemma 4.4 to remove left recursion
for i in V:
    # alpha contains all the alpha values i.e. alpha1, alpha2, ...
    # beta contains all the beta values i.e. beta1, beta2, ...
    alpha = []
    beta = []
    t = False
    prodt[i].sort()
    #print prodt, 'prod'
    for j in xrange(len(prodt[i])):
        x = prodt[i][j]
        #print 'x', x
        # first is a same variable (left recursion)
        # then store all the alpha and beta values
        if x[0] in V and x[0] == i:
            t = True
            alpha.append(x[1:])
        #elif t == True:
        else:
            beta.append(x)
        #print alpha
        #print beta, 'ab'
    # if alpha values present
    # performing the main operations of lemma 4.4
    index = V.index(i)
    if alpha:
        # new_beta contains all the productions where beta values are followed by new variable
        new_beta = []
        # new_alpha contains all the productions where alpha values are followed by new variable
        new_alpha = []
        prodt[i] = []
        # new variable (example if actual variable is A then new variable is A')
        new_var = letters[0]
        letters.remove(new_var)
        # adding new variable to main Variable list
        V.insert(index + 1, new_var)
        prodt[new_var] = []
        for k in beta:
            x = k+new_var
            new_beta.append(x)
        # merge two lists beta and new_beta
        #beta += new_beta
        # assign to the main productions
        prodt[i] = new_beta
        for k in alpha:
            x = k+new_var
            new_alpha.append(x)
        # merge two lists alpha and new_alpha
        #alpha += new_alpha
        # add productions of new variable to the main productions list
        prodt[new_var] = new_alpha + ['#']
#print prodt
### lemma 4.4 completed###
# output file
out_V = 'V : '+', '.join(V)
out_T = 'T : '+', '.join(T)
out_S = 'S : '+S
out_P = 'P : '
#output.write("After Using Lemma 4.4 for removing left recursions\n")
#output.write("# New Variables and Productions are :- \n")
output.write("%s\n" % out_V)
output.write("%s\n" % out_T)
output.write("%s\n" % out_S)
output.write("%s\n" % out_P)
for i in V:
    x = ' | '.join(prodt[i])    
    out_prod = i + ' -> '+ x
    output.write("%s\n" % out_prod)
#output.write("-----------------------------------------------------------------------------------------------------\n")
output.close()
