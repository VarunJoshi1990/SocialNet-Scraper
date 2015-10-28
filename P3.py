# -*- coding: utf-8 -*-
"""

@author: Varun Joshi
"""

import snap
import operator
import collections
import random

numnod=0
numedg=0
ugraph = snap.TUNGraph.New()
nodes = []

fin = open("An_Nodes.txt","rb")
for line in iter(fin):
    ugraph.AddNode(int(line))
    numnod+=1
    nodes.append(int(line))
fin.close() 

fin = open("An_Edges.txt","rb")
for line in iter(fin):
    ugraph.AddEdge(int(line.split(",",1)[0]),int(line.split(",",1)[1]))
    numedg+=1
fin.close() 


pg_vec = snap.TIntFltH() 
snap.GetPageRank(ugraph, pg_vec)

pg_dict = dict()

for item in pg_vec:
    pg_dict[item] = pg_vec[item]


pg_sort = sorted(pg_dict.values(), reverse = True)
pg_count10= 0
for value in pg_sort:
    for key1,val1 in pg_dict.iteritems():
        if val1 == value:
            print val1,key1
            pg_count10+=1
            break
    if pg_count10 == 10:
        break

evCntr_Vector = snap.TIntFltH() 
snap.GetEigenVectorCentr(ugraph, evCntr_Vector)

evCntr_dict = dict()

for item in evCntr_Vector:
    evCntr_dict[item] = evCntr_Vector[item]
    
evCntr_sort = sorted(evCntr_dict.values(), reverse = True)
evCntr_count10= 0
for value in evCntr_sort:
    for key1,val1 in evCntr_dict.iteritems():
        if val1 == value:
            print val1,key1 
            evCntr_count10+=1
            break
    if evCntr_count10 == 10:
        break

   

dc_dict = dict()
for nex in ugraph.Nodes():
    dc_dict[nex.GetId()] = snap.GetDegreeCentr(ugraph, nex.GetId())    

    

dc_sort = sorted(dc_dict.values(), reverse = True)
dc_count10= 0
dc_set = set(dc_sort)
dc_sort1 = sorted(list(dc_set), reverse = True)
for value in dc_sort1:
    for key1,val1 in dc_dict.iteritems():
        if val1 == value and dc_count10 < 10:
            print val1, key1
            dc_count10+=1
        if dc_count10 == 10:
            break
    if dc_count10 == 10:
        break
pg_rank_nodes = [None] * (len(nodes)+1)
count = 0    
it_r=iter(sorted(pg_dict.items(),key=operator.itemgetter(1)))
for item in it_r:
    
    pg_rank_nodes[item[0]] = (len(nodes)-count)
    count +=1
    
rank_e_nodes = [None] * (len(nodes)+1)
count = 0    
it_e=iter(sorted(evCntr_dict.items(),key=operator.itemgetter(1)))
for item in it_e:
    
    rank_e_nodes[item[0]] = (len(nodes)-count)
    count +=1


deg_r_nodes = [None] * (len(nodes)+1)
count = 0    
it1=iter(sorted(dc_dict.items(),key=operator.itemgetter(1)))
for nex in it1:    
    deg_r_nodes[nex[0]] = (len(nodes)-count)
    count +=1
     

sum_pe = 0
diff_pe = [None] * (len(nodes)+1)
sum_ed = 0
diff_ed = [None] * (len(nodes)+1)
sum_dp = 0
diff_dp = [None] * (len(nodes)+1)

for i in range(1,len(nodes) + 1):
    diff_pe[i] = (pg_rank_nodes[i]-rank_e_nodes[i]) ** 2
    sum_pe += diff_pe[i]
    diff_ed[i] = (rank_e_nodes[i]-deg_r_nodes[i]) ** 2
    sum_ed += diff_ed[i]
    diff_dp[i] = (deg_r_nodes[i]-pg_rank_nodes[i]) ** 2
    sum_dp += diff_dp[i]
    
n = len(nodes)
n2 = n *n

denom = n * (n2-1)

corr_pe = 1-(float(6*sum_pe)/float(denom)) 
corr_ed = 1-(float(6*sum_ed)/float(denom))
corr_dp = 1-(float(6*sum_dp)/float(denom))

print "The relation of pAgeRank with respect to eigen vector = ",corr_pe 
print "The relation of eigen vector with respect to deg centr= ",corr_ed
print "The relation of Deg Cent with respect to Page Rank is ",corr_dp


high_sim=0
node1=0
node2=0
k=0
for i in ugraph.Nodes():
    l=0
    for j in ugraph.Nodes():
        if(k==l):
            continue
        com=snap.GetCmnNbrs(ugraph, nodes[k], nodes[l])
        sim=float(com)/(i.GetOutDeg()+j.GetOutDeg()-com)
        if(sim>high_sim):
            high_sim=sim
            node1=i
            node2=j
        l+=1
    k+=1
print "Most similar nodes are "+ node1 +" and "+node2