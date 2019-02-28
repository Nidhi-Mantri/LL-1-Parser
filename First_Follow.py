import sys
from prettytable import PrettyTable

# for making dictionary of variable and corresponding productions
def Production_dict(P):
    prodt = {}
    for i in xrange(len(P)):
        x = P[i].split(' -> ')
        y = ''.join(x[1].split(' |')).strip('\n')
        y = y.split(' ')
        prodt[x[0]] = y
    return prodt

# generating first set of the variables
# V consists of all the variables in the grammar
# first_terms contains the first term of all the productions of the variable
# first_set will be the output
# pro_copy is the copy of prodt(the dictionary of the variables and their productions)
# x is the copy of first_terms
def First_Set(V, first_terms, first_set, x, pro_copy):
    for i in first_terms.keys():
        first_set[i] = [] #making empty list for first set of each variable
    for i in first_terms.keys():
        while x[i]:
            each = x[i][0] 
            if each not in V: # if terminal
                first_set[i].append(each)
            else:
                y = each # if each is a variable term
                #print 'each', each
                #print first_terms[y], 'x', y
                x[i].extend(first_terms[y]) # then add first terms of that variable to the first set...
                if '#' in x[i] : # if epsilon then put it and then get the next terminal or variable
                    for j in pro_copy[i]:
                        if j[0] == each and len(j)>1:
                            pro_copy[i].remove(j)
                            x[i].remove('#')
                            j = j[1:]
                            pro_copy[i].append(j)
                            x[i].append(j[0])
                # removing duplicate copies
                first_terms[i] = list(set(first_terms[i]))
            x[i].remove(each)
        # removing duplicate copies
        first_set[i] = list(set(first_set[i]))
    # returning the final output
    return first_set   

#  return all the productions in which the variable 'i' is present
def Productions_consisting(i, prodt) :
    productions = {}
    productions[i] = []
    other_v = prodt.keys()
    other_v.remove(i)
    # in the productions of the variable itself
    for j in prodt[i] :
        if i in j:
            productions[i].append(j)
    if not productions[i] :
        del productions[i]
    # in the productions of other variables
    for k in other_v :
        productions[k] = []
        for j in prodt[k]:
            if i in j:
                productions[k].append(j)
        if not productions[k] :
            del productions[k]
    return productions

# returns the follow set of the variables
# V consists of all the variables in the grammar
# first_set contains the first set of the variables
#follow_set will be the output
# i is the variable
# productions contains all the productions in which the variable 'i' is present
def Follow_Set(i, productions, follow_set, first_set, prodt, V):
    for k in productions.keys():
        while productions[k] :
            j = productions[k][0]
            # if the variable is the last of any production
            if i == j[-1] :
                follow_set[i].extend(follow_set[k])
                follow_set[i] = list(set(follow_set[i]))
            else :
                x = j.index(i) + 1
                # if next is a variable 
                if j[x] in V:
                    follow_set[i].extend(first_set[j[x]])
                    follow_set[i] = list(set(follow_set[i]))
                    if '#' in follow_set[i] :
                        follow_set[i].remove('#')
                        productions[k].append(j.replace(j[x], ''))
                # if next is a terminal
                else:
                    follow_set[i].append(j[x])
                    follow_set[i] = list(set(follow_set[i]))
            productions[k].remove(j)
    # returning the follow set
    return follow_set
    
def main():
    with open("Left_factoring_removed.txt", 'r') as input_file :
        V = input_file.readline().split(':')[1].strip(" \n")
        V = V.split(', ')
        T = input_file.readline().split(':')[1].strip(" \n")
        T = T.split(', ')
        S = input_file.readline().split(':')[1].strip(" \n")
        P = input_file.readlines()[1:]

    # assign all the productions to the variable in dictionary form
    prodt = Production_dict(P)
    pro_copy = Production_dict(P)
    # for first set
    first_set = {}
    first_terms = {}
    x = {}
    # finding first term of each production of the variable
    for i in prodt.keys():
        first_terms[i] = map(lambda e : e[0], prodt[i])
        x[i] = map(lambda e : e[0], prodt[i])    
    # first set of the variables
    first_set = First_Set(V, first_terms, first_set, x, pro_copy)
    #print "First_Set - > ", first_set
    # finding all the variables 
    var_s = prodt.keys()
    follow_set = {}
    # follow set of the variables    
    for i in var_s :
         follow_set[i] = [] 
    follow_set[S] = ['$'] 
    for i in V :
        productions = Productions_consisting(i, prodt)
        follow_set = Follow_Set(i, productions, follow_set, first_set, prodt, V)
    # repeatation
    for i in V :
        productions = Productions_consisting(i, prodt)
        follow_set = Follow_Set(i, productions, follow_set, first_set, prodt, V)
    #print "Follow_Set - > ",follow_set    
    first_table = PrettyTable()
    first_table.field_names = ['V', 'First']
    follow_table = PrettyTable()
    follow_table.field_names = ['V', 'Follow']
    for i in var_s:
        first_table.add_row([i, first_set[i]])
        follow_table.add_row([i, follow_set[i]])
    output = open("Output.txt", 'w')
    output.write("First Set -> \n%s\n" % first_table)
    output.write("Follow Set -> \n%s\n" % follow_table)
    # parsing table generation
    # Step - 4
    # creating a table for output
    term_s =  T+['$']
    table = {}
    for v in V:
        table[v] = {}
        for t in term_s:
            table[v][t] = []
        for j in prodt[v]:
            if j[0] in V:
                for k in first_set[j[0]]:
                    if k != '#' :
                        table[v][k].append(j)
                        table[v][k] = list(set(table[v][k]))
                    else:
                        for l in follow_set[v]:                        
                            table[v][l].append(j)
                            table[v][l] = list(set(table[v][l]))
            elif j[0] == '#' :
                for l in follow_set[v]:
                        table[v][l].append(j)
                        table[v][l] = list(set(table[v][l]))
            else:
                table[v][j[0]].append(j)
                table[v][j[0]] = list(set(table[v][j[0]]))
    # printing the output
    output.write('----------------------------------------\n')
    output.write('Parsing Table -> \n')
    output.write('-----------------------------------------\n')
    max_ = 0
    for k in table.keys():
        output.write('[%s] -> \n' % str(k))
        output.write('-------------------------------\n')
        for l in table[k].keys():
            if table[k][l]:
                length = len(table[k][l])
                if length > max_ :
                    max_ = length
                output.write('||  [%s]  -> ' % str(l))
                x = ' | '.join(table[k][l])
                out_prod = k + ' -> '+ x
                output.write('[%s]\n' % out_prod)
        output.write('-------------------------------\n')
    if max_ > 1:
        output.write('Since there are multiple entries in the table, ...\n')
        output.write("LL(1) Parser can't be constructed for this grammar.\n")
    else:
        output.write('LL(1) Parser is constructed for this grammar\n')
            
            
if __name__ == '__main__' :
    main()
