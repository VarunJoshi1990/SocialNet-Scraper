# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 11:12:16 2015

@author: Varun Joshi
"""

import snap
import collections
import random

numnod=0
numedg=0
ugraph = snap.TUNGraph.New()
fin = open("An_Nodes.txt","rb")
for line in iter(fin):
    ugraph.AddNode(int(line))
    numnod+=1
fin.close() 

fin = open("An_Edges.txt","rb")
for line in iter(fin):
    ugraph.AddEdge(int(line.split(",",1)[0]),int(line.split(",",1)[1]))
    numedg+=1
fin.close() 


triads = snap.GetTriads(ugraph)
print "triads : ",triads

EdgeV = snap.TIntPrV()
snap.GetEdgeBridges(ugraph, EdgeV)
print "bridges : ",len(EdgeV)

diameter = snap.GetBfsFullDiam(ugraph, 50)
print "diameter : ",diameter

snap.PlotInDegDistr(ugraph,"degDist","degDist")

u_edges = dict()
fin = open("An_Edges.txt","rb")
cnt = 1
for n in iter(fin):
    u_edges[cnt] = str(n)
    cnt += 1
fin.close() 

u_scc = dict()
for p in range(100, 0, -1):
    u_removal_graph = snap.TUNGraph.New()
    fin = open("An_Nodes.txt","rb")
    for n in iter(fin):
        u_removal_graph.AddNode(int(n))
    fin.close() 
    
    if p == 100:
        csize = snap.GetMxWcc(u_removal_graph)
        lcsize = snap.CntNonZNodes(csize)
    else:
        toAdd = ((100-p)* (cnt-1))/100 
        random_edges = random.sample(xrange(1,cnt-1),toAdd)
        for edge_num in random_edges:
            ln = u_edges.get(edge_num)
            u_removal_graph.AddEdge(int(ln.split(",",1)[0]),int(ln.split(",",1)[1]))
        csize = snap.GetMxWcc(u_removal_graph)
        lcsize = snap.CntNonZNodes(csize)
    u_scc[p] = lcsize    

print "\n"
for k1,v1 in u_scc.iteritems():
    print k1, v1
