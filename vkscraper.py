# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 17:46:14 2015

@author: Varun Joshi
"""

import urllib, json
import psycopg2


user='postgres'
password='root'
dbname='postgres'
con=psycopg2.connect("dbname='" + dbname + "' user='" + user + "' host='localhost' password='" + password + "'")
cur=con.cursor()

api="https://api.vk.com/method/"
#dict = {};
visited=[]
count=1
index=0
new_ind=0

def isVisited(uid):
    i=0    
    while i<index:
        if(visited[i]==uid):
            return i+1
        i+=1
    return 0
    
def user_id(uid):
    node=open("C:\Personal\Academics\Fall 2015\SMM\Project\\vk\\TNodesNew.txt","ab")
    print api+'users.get?user_ids='+str(uid)
    flag=0
    while(flag==0):    
        try:
            raw=urllib.urlopen(api+'users.get?user_ids='+str(uid))
            flag=1
        except IOError:
            time.sleep(20)
            flag=0
            
    data=json.load(raw)
    name=data['response'][0]['first_name'] + ' ' +data['response'][0]['last_name']
    name=name.replace("'","")
    print str(uid)+','+str(count)+'\n'
    node.write(str(uid)+','+str(count)+'\n')
    insert='insert into nodesnew (vkid,aid) values (' + str(uid) +','+str(count) +')'
    cur.execute(insert)
    con.commit()
    node.close
    #print data
    
def get_friends(uid):
    global new_ind
    nodes=open("C:\Personal\Academics\Fall 2015\SMM\Project\\vk\\All.txt","ab")
    edge=open("C:\Personal\Academics\Fall 2015\SMM\Project\\vk\\Edges.txt","ab")
    aedge=open("C:\Personal\Academics\Fall 2015\SMM\Project\\vk\\A_Edges.txt","ab")
    sam=open("C:\Personal\Academics\Fall 2015\SMM\Project\\vk\\Sample.txt","ab")
    asam=open("C:\Personal\Academics\Fall 2015\SMM\Project\\vk\\A_Sample.txt","ab")
    print api+'friends.get?user_id='+str(uid)
    raw=urllib.urlopen(api+'friends.get?user_id='+str(uid))
    flist=json.load(raw)    
    if(flist.has_key('error')):
        return 1
    friends=flist['response']
    i=0
    l=len(friends)
    print len(friends)
    if(l>1000):
        insert='insert into sample (node,edge) values (' + str(uid)+','+str(l) +')'
        cur.execute(insert)
        insert='insert into a_sampled (node,edge) values (' + str(count)+','+str(l) +')'
        cur.execute(insert)
        con.commit()
    
    while i< l and i<1000:
        ind=isVisited(friends[i])
        edge.write(str(uid)+','+str(friends[i])+'\n')
        insert='insert into newedges (e1,e2) values (' + str(uid)+','+str(friends[i]) +')'
        cur.execute(insert)
        con.commit()
        if(ind==0):
            new_ind+=1
            aedge.write(str(count)+','+str(new_ind)+'\n')
            insert='insert into an_newedge (e1,e2) values (' + str(count)+','+str(new_ind) +')'
            cur.execute(insert)
            visited.append(friends[i])
            nodes.write(str(friends[i])+'\n')            
        else:
            aedge.write(str(count)+','+str(ind)+'\n')
            insert='insert into an_newedge (e1,e2) values (' + str(count)+','+str(ind) +')'
            cur.execute(insert)
        i+=1
        con.commit()
    print friends
    nodes.close
    edge.close
    aedge.close
    sam.close
    asam.close
    return 0
    
visited.append(12010003)
read=open("C:\Personal\Academics\Fall 2015\SMM\Project\\vk\\All.txt","rb")
for line in read:
    visited.append(int(line.strip()))
while(count<=1000):
    curr=visited[index]
    check=isVisited(curr)
    if check!=0:
        index+=1
        continue
    access=get_friends(curr)
    if(access==1):
        index+=1
        continue
    user_id(curr)
    count+=1
    index+=1

while(index<len(visited)):
    curr=visited[index]
    check=isVisited(curr)
    if check!=0:
        index+=1
        continue
    user_id(curr)
    count+=1
    index+=1
