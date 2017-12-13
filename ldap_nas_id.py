
# coding: utf-8

# In[47]:


from functools import partial
from multiprocessing.pool import Pool
import ldap
from ldap3 import Server, Connection, ALL,SUBTREE
import  time
import asyncio
import time
import datetime
import threading
import pickle
SVLDAP='127.0.0.1:1389'
PHLDAP='127.0.0.1:2389'
SVdict={}
PHdict={}
data={}
username = "uid=freeradius,ou=admin,o=TE Data,c=eg" 
password = "xxxx"
s=Server
c=Connection
#print("test1")


# In[59]:


def initlize_connection(lserver):
    print("Trying to Conect to {}".format(lserver))
    username = "uid=freeradius,ou=admin,o=TE Data,c=eg" 
    lpassword = "ld4pm1gration"
    
    s = Server(lserver, get_info=ALL)
    c = Connection(s, user=username, password=lpassword)
    if not c.bind():
        print('error in bind', c.result)
        initlize_connection(lserver)
    
def get_nasid(lserver,user_name):
    username = "uid=freeradius,ou=admin,o=TE Data,c=eg" 
    lpassword = "xxxx"
    s = Server(lserver, get_info=ALL)
    c = Connection(s, user=username, password=lpassword)
    if not c.bind():
        print('error in bind', c.result)
        initlize_connection(lserver)
    
    
    try:
        c.search(search_base='ou=corporate,ou=email,o=TE Data,c=eg',
         search_scope=SUBTREE,search_filter='(uid='+user_name+')' ,
                   attributes = ['radiusCheckItem','mail'])
        return c.response[0]['attributes']['radiusCheckItem'][0][15:-1]
    except:
        print (c.response)
        return (user_name)
#get_nasid(SVLDAP,'3835995@tedata.net.eg')



# In[49]:


#c.closed
#c.unbind()
# if not c.bind():
#         print('error in bind', c.result)
#         initlize_connection(SVLDAP)



# In[50]:


# c.search(search_base='ou=corporate,ou=email,o=TE Data,c=eg',
#          search_scope=SUBTREE,search_filter='(uid='+user_name+')' ,
#                    attributes = ['radiusCheckItem','mail'])
# c.response[0]['attributes']['radiusCheckItem'][0][15:-1]


# In[51]:



# #ldapsearch -D "uid=freeradius,ou=admin,o=TE Data,c=eg" -w ld4pm1gration -p 2389 -h 127.0.0.1
# #-b  "ou=corporate,ou=email,o=TE Data,c=eg" "uid=2456630@tedata.net.eg"

# def get_nasid(lserver,user_name):
# #    print (user_name)

# #    user_name=user_name.strip()
# #    print('ffffffffffff')
# #    print (clean_user_name(user_name))

#     l = ldap.initialize('ldap://'+lserver)
#     username = "uid=freeradius,ou=admin,o=TE Data,c=eg" 
#     password = "ld4pm1gration"
#     try:
#         l.protocol_version = ldap.VERSION3
#         l.simple_bind_s(username, password)
#         valid = True
#         s= l.search_s('ou=corporate,ou=email,o=TE Data,c=eg',ldap.SCOPE_SUBTREE,'uid='+user_name,['radiusCheckItem','mail'])
#         #print(lserver)
# #         if lserver==PHLDAP:
# #             #PHdict[user_name]=str(s[0][1]['radiusCheckItem'])[18:-3]
# #         elif lserver==SVLDAP:
# #             #SVdict[user_name]=str(s[0][1]['radiusCheckItem'])[18:-3]
# #         else:
# #             print(lserver)
#         return str(s[0][1]['radiusCheckItem'])[18:-3]
#     except IndexError:
#         return str('No Data Found')
# #     except FILTER_ERROR:
# #         return ('FILTER_ERROR')
#         #if '\\t' in user_name:
#             #user_name.rplace('\\t',"")
#             #prit('\\t')
#     except Exception as e:
#          #print ("error")
#         return str('wrong_user_name '+user_name)
#         #return
#         #raise
# get_nasid(PHLDAP,'3835995@tedata.net.eg')


# In[52]:


def get_nasid2(lserver,user_name):
    l = ldap.initialize('ldap://'+lserver)
    if not data[user_name]:
        data[user_name]=[]

    try:
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(username, password)
        valid = True
        s= l.search_s('ou=corporate,ou=email,o=TE Data,c=eg',ldap.SCOPE_SUBTREE,'uid='+user_name,['radiusCheckItem','mail'])
                #print(lserver)
        results=str(s[0][1]['radiusCheckItem'])[18:-3]    
        d={}
        if lserver==PHLDAP:
            
            d['PHLDAP']= results
            data[user_name].append(d)
            return results
        elif lserver==SVLDAP:
            d['SVLDAP']= results
            data[user_name].append(d)
            return results
        #return str(s[0][1]['radiusCheckItem'])[18:-3]
    except IndexError as e:
        return str('No Data Found')
#        return e
    except Exception as e:
        #return str('wrong_user_name '+user_name)
        return str(e)
        #return r
    

# get_nasid2(PHLDAP,'3835995@tedata.net.eg')
# get_nasid2(SVLDAP,'3835995@tedata.net.eg')
# data


# In[53]:


# if data['446627r7@tedata.net.eg']:
#     print('e')
# #{username:{ph:ff},{SV:gg}}


# In[54]:


# SVD={}
# PHD={}
# ALLsites={"username":[["SV"],["PH"]]}
# def coroutine(func):
#     def start(*args,**kwargs):
#         cr=func(*args,**kwargs)
#         #cr.__next__()
#         next(cr)
#         return cr
#     return start
    

    
    
# @coroutine
# def stc_getusernasfromSV():
#     try:
#         while True:
#             username=(yield)
#             #print('Corotine  SV Username {}'.format(username))
#             #SVD[username]=(get_nasid(SVLDAP,username))
#             sl5
            
#     except StopIteration:
#             print("Stop")
            
# @coroutine
# def stc_getusernasfromPH():
#     try:
#         while True:
#             username=(yield)
#             #print('Corotine  PH Username {}'.format(username))
#             #PHD[username]=(get_nasid(PHLDAP,username))
#             sl8
            
#     except StopIteration:
#             print("Stop")
            
# def g1(username,targets=[stc_getusernasfromSV(),stc_getusernasfromPH()]):
#     #print("Generator Started")
#     while username:
#         #print ("Generator"+username)
#         for i in targets:
#             i.send(username)
#         username=None
            
# # @coroutine
# # def compsites():
# #     ALLsites[username]=yield
# #     if SVD[]==PHD["4466277@tedata.net.eg"]:
# #         print('True')
# #     else:
# #         print("False")
    
   


# In[55]:


# def mygenerator(x,target):
#     while True:
#         target.send(x)
    
# #@coroutine
# def sl5():
#     s=datetime.datetime.now()
#     time.sleep(5)
#     e=datetime.datetime.now()
#     print(e-s)
#     print("5")
# def sl8():
#     s=datetime.datetime.now()
#     time.sleep(8)
#     e=datetime.datetime.now()
#     print(e-s)
#     print("8")
    
# def r(list1):
#     for i in list1:
#          yield i()

# rr=r([sl8,sl5])
# #sl8()
# #sl5()
# #d=mygenerator(4,sl5)


# In[56]:


# for i in rr:
#     next(i)


# In[57]:


#c=stc_getusernasfromSV()
#c.send("2456630@tedata.net.eg")
#g1("4466277@tedata.net.eg",[stc_getusernasfromSV(),stc_getusernasfromPH()])
#GG
#print(SVD)
#print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
#print(PHD)



# In[26]:


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


# In[27]:


#


# In[28]:


# s=threading.Thread(target=svget, args=('4466277@tedata.net.eg',))
# s.start()
# #threading.Thread(target=svget, args=('4466277@tedata.net.eg',)).join()


# In[29]:


# p=pickle.load(open('pickle1','rb'))
# p=p.tolist()


# In[30]:


# len(p)
# svlist=[]
# phlist=[]


# In[31]:


# svget('3835995@tedata.net.eg')


# In[32]:



# svget=partial(get_nasid,SVLDAP)
# phget=partial(get_nasid,PHLDAP)
# #phget('3835995@tedata.net.eg')
# #svget('3835995@tedata.net.eg')


# In[33]:


# def svsequentila(l):
    
#     for i in l:
#         svlist.append(svget(i))
# %time(svsequentila(p))    


# In[34]:


# def phsequentila(l):
    
#     for i in l:
#         phlist.append(phget(i))
# %time(phsequentila(p))    


# In[35]:


#sphlist


# In[36]:


#####################TOPTAL Exampl####################

# listt=[]
# def main():
#     with Pool(300) as p:
#         listt.append(list(map(svget,lp)))
            

# main()
# #listt
#len(listt[0])


# In[37]:


# thread_list = []

# for i in p:
#     # Instantiates the thread
#     # (i) does not make a sequence, so (i,)
#     svt = threading.Thread(target=svget, args=(i,))
#     #pht = threading.Thread(target=phget, args=(i,))

#     # Sticks the thread in a list so that it remains accessible
#     thread_list.append(svt)
#     #thread_list.append(pht)


# # Starts threads
# for thread in thread_list:
#     thread.start()

# # This blocks the calling thread until the thread whose join() method is called is terminated.
# # From http://docs.python.org/2/library/threading.html#thread-objects
# for thread in thread_list:
#     thread.join()

# # Demonstrates that the main process waited for threads to complete
# print ("Done")


# In[38]:


#len(SVdict)


# In[39]:


#len(PHdict)


# In[40]:


# from multiprocessing.pool import ThreadPool as Pool

# pool_size =4   # your "parallelness"
# pool = Pool(pool_size)


# def worker(lserver,user_name):
#     #print(lserver)

#     try:
#         #print('fff')
#         if lserver==SVLDAP:
#             print('qqq')
#             SVD[user_name]=get_nasid(SVLDAP,user_name)
#         elif lserver== PHLDAP:
#             PHD[user_name]=get_nasid(PHLDAP,user_name)
#         else:
#             print('Else')
#     except:
#         print('error with item')


# for item in p:
#     #print(item)
#     pool.apply_async(worker(PHLDAP,item), (item,))

# pool.close()
# pool.join()


# In[41]:


#SVD


# In[42]:



# def filldicts(user_name):
#     s1=[]
#     s2=[]
#     t1=threading.Thread(target=get_nasid,args=(PHLDAP,user_name,))
#     s1.append(t1)
#     t2=threading.Thread(target=get_nasid,args=(SVLDAP,user_name,))
#     s2.append(t2)

#     t1.start()
#     t2.start()
#     t1.join()
#     t2.join()

    
# #filldicts('645970@tedata.net.eg')
# print(len(SVdict),len(PHdict))


# In[43]:


# # myl=[x for x in range(2000)]
# # for i in myl:
# #     filldicts(str(i))
# # SVdict
# SVdict={}
# PHdict={}
# for i in p[0:50]:
#     filldicts(i)
# len(PHdict)


# In[44]:


#print(len(SVdict),len(PHdict))


# In[45]:


#PHdict


# In[46]:


# def compardicts(user_name):
    
#     return [PHdict[user_name] ,SVdict[user_name],
#             PHdict[user_name] == SVdict[user_name] ]
        
# #x,y,z=compardicts('645970@tedata.net.eg\t')  
# #print(x,y,z)


# In[50]:


#PHdict.keys()


# In[51]:


#l.bind="ou=corporate,ou=email,o=TE Data,c=eg"


# In[52]:


#l.search("uid=2456630@tedata.net.eg",0)
#l.search_s("uid=2456630@tedata.net.eg", ldap.SCOPE_SUBTREE,"uid=2456630@tedata.net.eg","radiusCheckItem")


#help(l.search_st


# In[53]:


# SVD={"username":"nid"}
# PHD={"username":"nid"}


# In[54]:


# d={}
# d["ww"].append(33)


# In[55]:



#d['ww'].insert (3)

