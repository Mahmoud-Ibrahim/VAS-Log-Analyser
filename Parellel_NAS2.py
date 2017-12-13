
# coding: utf-8

# In[19]:


from functools import partial
from multiprocessing import Lock, Process, Queue, current_process,pool
import ldap
import asyncio
import time
import datetime
import threading
import pickle
from ldap_nas_id  import *
import os
import signal
import pandas as pd
import collections

#import ldap3
SVLDAP='127.0.0.1:1389'
PHLDAP='127.0.0.1:2389'
# SVdict={}
# PHdict={}
# data={}
svget=partial(get_nasid,SVLDAP)
phget=partial(get_nasid,PHLDAP)
inq=Queue()
outq=Queue()
Process.daemon = True
results=[]


# In[20]:


usernas=collections.namedtuple("usernas","username PHnas SVnas")
#usernas("3773454@tedata.net.eg","ddd","ffffff")


# In[21]:


# p=pd.read_pickle('pickle1')
# #p=pickle.load(open('pickle1','rb'))
# p=p.tolist()
# lp=p[0:500]
# #lp=lp*100
# len(lp)


# In[22]:


#len(lp)


# In[23]:


# for i in lp:
#     inq.put(i)
# inq.qsize()


# In[24]:


def myworker(username):
    #for i in range(inq.qsize()):
        #us=inq.get()
        us=usernas(username,svget(username),phget(username))
        #print(us)
        outq.put(us)
#myworker(inq,outq)    


# In[25]:


# for i in range(q11.qsize()):
#     print(q11.get())
def main(lp,worker_count=20):
    
    with Pool(worker_count) as workers:
        workers.map(myworker, lp)
        for i in range(outq.qsize()):
            results.append(outq.get())
    



# In[1]:


#main(lp)


# In[2]:


#results


# In[3]:


# for i in results:
#     if i.PHnas==i.SVnas:
#         print ("OK")


# In[4]:


#results[0].username


# In[43]:



# def dividelist(mylist,n):
#     startpoint=0
#     while startpoint < len(mylist):
#         if len(mylist[startpoint:])> n:
#             yield mylist[startpoint:startpoint+n]
#             startpoint=startpoint+n
#             #print(startpoint)

#         else:
#             yield mylist[startpoint:]
#             startpoint=len(mylist)
#             #yield ("ddddddddd")
# #list1=[1,2,3,4,5,6,7,8,9]
# #d=dividelist(list1,4)


# In[7]:


# def SVworker(inpuque,done_queue):
    
#     try:
#         for user in iter(inpuque.get, 'STOP'):
#             #done_queue.put([user,svget(user)])
#             l=[user,svget(user)]
#             done_queue.put(l)
#             #yield (work_queue.qsize())
#     except Exception as e:
#         done_queue.put("%s failed on %s with: %s" % (current_process().name, "error", e.message))
#     #testlist.append(done_queue.get())
#     #return True
# def PHworker(inpuque,doneque):
    

#     try:
#         for user in iter(inpuque.get, 'STOP'):
#             doneque.put([user,phget(user)])
#     except Exception as e:
#         done_queue.put("%s failed on %s with: %s" % (current_process().name, "error", e.message))
# #     testlist.append(done_queue.get())
# #     print(testlist)

#     #return True


# In[8]:


# #listdone=[]


# def main(looplist,site):
#     workers = 20
#     global processes
#     processes = []   

#     for user in looplist:
#         #print(user)
#         work_queue.put(user)
#     #work_queue.put('STOP')
#     #print(work_queue.qsize())
#     #print("starting Wokers")
#     if site=='SV':
#         s=SVworker
#         print("Smat worker")
#     elif site=='PH':
#         print("PH worker")
#         s=PHworker
        
#     for w in range(workers):
#         p = Process(target=s, args=(work_queue, done_queue))
# #         print("Work Queue count  : {}".format(work_queue.qsize()))
# #         print("Done  Queue count  : {}".format(done_queue.qsize()))
        
#         p.start()
#         processes.append(p)
# #     print("#################Work Queue count  : {}".format(work_queue.qsize()))
# #     print("#################Done  Queue count  : {}".format(done_queue.qsize()))
# #     for p in processes:
# #         p.pid
# #         #p.join_thread()
# #     print("start Closing")
# #     work_queue.close()
# #     print("Thread Closing")
# #     work_queue.join_thread()
# #     print("Thread Joined")

    
#         #listdone.append(done_queue.get())
#         #p.terminate()

#         #p.join()

#         #p.terminate()
    
# #     for p in processes:
# #         print("Before Joing processs")
# #         p.terminate()
# #    done_queue.put('STOP')


# In[17]:


#main(lp,'SV')


# In[18]:


#done_queue.qsize()


# In[19]:


#work_queue.qsize()


# In[9]:


# def getlistnas(site,ulist,chunk):
#     global work_queue
#     global done_queue
#     work_queue = Queue()
#     done_queue = Queue()
#     rlist=[]
#     looplist=dividelist(ulist,chunk)
#     for i in looplist:
#         main(i,site)
#         time.sleep(.5)
#         print("Waiting 1 Sec")
#     #print(work_queue.qsize())

#     while work_queue.qsize() > 0:
#         print("----------------------Work Queue count  : {}".format(work_queue.qsize()))
#         print("----------------------Done  Queue count  : {}".format(done_queue.qsize()))
#         time.sleep(5)
    
# #    print( work_queue.empty())

#     #continue
# #     while True:
# #         print("Inside while")
# #         if work_queue.qsize() > 0:
# #             print("Wating for  work que to be Done ")
# #             print(work_queue.qsize())
# #             time.sleep(5)
# #             continue
# #         break
# #     for p in processes :
# #         p.terminate()

#     done_queue.put('STOP')
#     #print("Terminating Processes")
# ############################################################
# #    print("Done Queue Count IS {}".format(done_queue.qsize()))
# #    for user in iter(done_queue.get, 'STOP'):
#     for user in range(done_queue.qsize()):
#         rlist.append(done_queue.get())
# #     for i in range(len(lp)):
# #         rlist.append(done_queue.get())
# ####################################################    
#     #done_queue.qsize()
#     print( "work Queue Empty is :  {}".format(work_queue.empty()))
# #     print('tarting Killing')
# #     work_queue.close()
# #     work_queue.join_thread()
# #     for p in processes:
# #                 print(p)
# #                 #p.join()
# #                 p.terminate()
# #                 time.sleep(1)
#     for i in processes:
        
#         i.terminate()
#         #print (i.pid)
#         os.kill(i.pid, signal.SIGKILL)
    
#     return rlist
# # while   work_queue.empty():
              
# #    for p in processes:
#         #print(p)
# #        p.terminate()
#         #processes
#         #print(p)

# #         break
# # processes
# # processes
# #len(listdone)
# #testlist=[]


# In[44]:


# %time phlist=getlistnas('PH',lp,500)


# In[22]:


# for i in processes:
#     i.terminate()
#     #print (i.pid)
#     os.kill(i.pid, signal.SIGKILL)


# In[45]:


#processes


# In[24]:


# for p in processes:
#             print(p)
#             p.terminate()
#             processes
#             #print(p)
#processes        


# In[27]:


#%time SVlist=getlistnas('SV',lp,500)


# In[ ]:


#work_queue.qsize()
#ss=SVlist


# In[ ]:


#pp=phlist


# In[ ]:


# for i in range( len(ss)):
#     #print(ss[i])
#     print(i)
#     if pp[i][0] == ss[i][0]:
#         if pp[i][1] != ss[i][1]:
#             print([pp[i],ss[i]])
#     else:
#         print ("Mismatched Order ")


# In[47]:


# def compare_stes(SVlist,phlist):
#     return [x for x in SVlist if not x in phlist],[x[1] for x in phlist if not x in SVlist]
# ##[x[]for x in ss if not x in pp],[x[1] for x in pp if not x in ss]


# In[48]:


#compare_stes(SVlist,phlist)


# In[49]:


# from multiprocessing.pool import ThreadPool as Pool

# pool_size =100   # your "parallelness"
# pool = Pool(pool_size)

# def worker(lserver,user_name):
#     #print(lserver)

#     try:
#         if lserver==SVLDAP:
#             SVdict[user_name]=get_nasid(SVLDAP,user_name)
#         elif lserver== PHLDAP:
#             PHdict[user_name]=get_nasid(PHLDAP,user_name)
#         else:
#             print('Else')
#     except Exception as e:
#         print(e)

# with Pool(80) as p:
#       #p.map(svget, lp)
#     p.apply_async(worker(PHLDAP,item), (item,))

# #def startprocesses():

# # for item in p:
# #     #print(item)
# #     pool.apply_async(worker(PHLDAP,item), (item,))
# #     pool.apply_async(worker(SVLDAP,item), (item,))

# # pool.close()
# # pool.join()
# #SVdict


# In[50]:


# def comparesites(user_name):
#     SVID= get_nasid(SVLDAP,user_name)
#     PHID=get_nasid(PHLDAP,user_name)
#     return [SVID==PHID,SVID,PHID]
# #    if SVid==PHID:
# #    return True
# #    else:
# #        return False

# #comparesites('645970@tedata.net.eg\t')    
# #SVdict
# #comparesites('admin') 
# threadlist=[]

# def getresultsp(user_name):
#     threadlist.append(threading.Thread(target=svget, args=(user_name,)))
#     threadlist.append(threading.Thread(target=phget, args=(user_name,)))
#     for i in threadlist:
#         i.start()
#     mr='f'
#     svr='g'
#     phr='2'
#     return user_name,phr,svr,mr
# #getresultsp('4466277@tedata.net.eg')


# In[51]:


#len(lp)

