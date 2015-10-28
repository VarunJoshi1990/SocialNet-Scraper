# -*- coding: utf-8 -*-
"""
@author: Varun Joshi
"""

import snap
import collections
import random
import operator

numnod=0
numedg=0
ugraph = snap.TUNGraph.New()
node_list = []

fin = open("An_Nodes.txt","rb")
for line in iter(fin):
    ugraph.AddNode(int(line))
    numnod+=1
    node_list.append(int(line))
fin.close() 

fin = open("An_Edges.txt","rb")

for line in iter(fin):
    ugraph.AddEdge(int(line.split(",",1)[0]),int(line.split(",",1)[1]))
    numedg+=1
fin.close() 


rand_grph= snap.GenRndGnm(snap.PUNGraph,numnod,numedg,False)
snap.PlotInDegDistr(rand_grph,"degDistRand","degDistRand")
#rand_grph.GetBfsEffDiam(ugraph,1,False,)
clust=snap.GetClustCf(rand_grph)
print "C Coeff Rand" + str(clust)



pref_grph= snap.GenPrefAttach(numnod,4)
snap.PlotInDegDistr(pref_grph,"degDistPref","degDistPref")
clust=snap.GetClustCf(pref_grph)
print "C Coeff Pref" + str(clust)


prob=(float(numnod)/(numedg*(numedg-1)))*2
print prob
smal_grph=snap.GenSmallWorld(numnod,4,prob)
snap.PlotInDegDistr(smal_grph,"degDistSmal","degDistSmal")
clust=snap.GetClustCf(smal_grph)
print "C Coeff Small" + str(clust)
