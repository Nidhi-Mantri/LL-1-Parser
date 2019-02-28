import sys
from collections import Counter

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = list(letters)

def Production_dict(P):
    prodt = {}
    for i in xrange(len(P)):
        x = P[i].split(' -> ')
        y = ''.join(x[1].split(' |')).strip('\n')
        y = y.split(' ')
        prodt[x[0]] = y
    return prodt

def factoring(v, prodt, Var_s, V):
    size_pro = {}
    pr_copy = prodt[v][:]
    while pr_copy:
        # smallest of the productions
        smallest_str = min(pr_copy, key=len)
        # size of the production
        size = len(smallest_str)
        act_size = len(smallest_str)
        if size in size_pro.keys():
            while size in size_pro.keys():
                size += 1
        size_pro[size] = []
        # copy of prod
        others = prodt[v][:]
        # contain all the productions except the smallest one
        others.remove(smallest_str)
        #print 'others', others
        # creating dictionary on the basis of size and same prefixed productions
        for each in others :
            if each[:act_size] == smallest_str :
                size_pro[size].append(each)
                pr_copy.remove(each)
        #print size_pro[size], 'del'
        if not size_pro[size] :
            #print size_pro[size], 'dfd'
            del size_pro[size]
        else:
            size_pro[size].append(smallest_str)
        pr_copy.remove(smallest_str)

    # removing left factoring
    for i in size_pro.keys():
        new_p = min(size_pro[i], key=len)
        size = len(new_p)
        new_prod = []
        for j in size_pro[i]:
            #print new_p, j
            # if the same production
            if new_p == j:
                new_prod.append('#')
            else:
                new_prod.append(j[size:])
            #print j, prodt[v]
            prodt[v].remove(j)
            #size_pro[i].remove(j)
        new_v = letters[0]
        letters.remove(new_v)
        Var_s.append(new_v)
        V.append(new_v)
        prodt[v].append(new_p+new_v)
        prodt[new_v] = new_prod
    return prodt, Var_s, V

def main():
    with open("Recursion_removed.txt", 'r') as input_file :
        x = input_file.readline()
        if 'Error' in x :
            print "Aborted"
            sys.exit()
        else:
            V = x.split(':')[1].strip(" \n")
            V = V.split(', ')
            T = input_file.readline().split(':')[1].strip(" \n")
            T = T.split(', ')
            S = input_file.readline().split(':')[1].strip(" \n")
            P = input_file.readlines()[1:]
    for i in V:
        letters.remove(i)
    # assign all the productions to the variable in dictionary form
    prodt = Production_dict(P)
    Var_s = V[:] 
    while Var_s:
        prodt, Var_s, V = factoring(Var_s[0], prodt, Var_s, V)
        del Var_s[0]
    print V
    print prodt
    #factoring_removed = Left_Factoring(V, prodt)
    output = open("Left_factoring_removed.txt", 'w')
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

if __name__ == '__main__' :
    main()
