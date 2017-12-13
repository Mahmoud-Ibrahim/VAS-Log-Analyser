
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import Pymailer
import pynliner
import matplotlib.pyplot as plt
import gzip,csv
import os
import ldap_nas_id
pd.set_option('max_colwidth',170)
import pymongo
#import Parellel_NAS
import Parellel_NAS2
#%matplotlib inline
try:
    import MySQLdb
except:
    import pymysql as MySQLdb
    #pymysql.install_as_MySQLdb() 
    #https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python
import threading



# In[4]:


def fill_frommysql(file_name):
    db = MySQLdb.Connect("127.0.0.1","operation","xx","sbr_vaslog",port=3150
                         )
    cursor = db.cursor()
    sqlquery="select * from VAS_Log  where  date_time > DATE_SUB(NOW(), INTERVAL 6 hour)"
    #cursor = db.cursor(cursorclass=MySQLdb.cursors.SSDictCursor)
    cursor.execute(sqlquery)
    #with open(file_name,"w") as f:
    writer=csv.writer(open(file_name,"w"))
    #print(cursor.)
    writer.writerow([i[0] for i in cursor.description])
    for row in cursor:
        writer.writerow(row)
        #print(row)

    cursor.close()
    db.close()
t=threading.Thread(target=fill_frommysql,args=("../Files/vasloghourly.csv",))
t.start()
t.join()


#######################################################################################
def fillWifi_frommysql(file_name):
    db = MySQLdb.Connect("127.0.0.1","operation","xx$$","tewifi",port=3150
                         )
    cursor = db.cursor()
    sqlquery="select * from wifi_wifilogs  where  timestamp > DATE_SUB(NOW(), INTERVAL 6 hour)"
    #cursor = db.cursor(cursorclass=MySQLdb.cursors.SSDictCursor)
    cursor.execute(sqlquery)
    #with open(file_name,"w") as f:
    writer=csv.writer(open(file_name,"w"))
    #print(cursor.)
    writer.writerow([i[0] for i in cursor.description])
    for row in cursor:
        writer.writerow(row)
        #print(row)

    cursor.close()
    db.close()
t=threading.Thread(target=fillWifi_frommysql,args=("../Files/Wifi.csv",))
t.start()
t.join()


#######################################################################################
#select * from wfws_mactal where date_time > DATE_SUB(NOW(), INTERVAL 6 minute
def fillmac_frommysql(file_name):
    db = MySQLdb.Connect("127.0.0.1","operation","xx$$","tewifi",port=3150
                         )
    cursor = db.cursor()
    sqlquery="select * from wfws_mactal where date_time > DATE_SUB(NOW(), INTERVAL 6 hour)"
    #cursor = db.cursor(cursorclass=MySQLdb.cursors.SSDictCursor)
    cursor.execute(sqlquery)
    #with open(file_name,"w") as f:
    writer=csv.writer(open(file_name,"w"))
    #print(cursor.)
    writer.writerow([i[0] for i in cursor.description])
    for row in cursor:
        writer.writerow(row)
        #print(row)

    cursor.close()
    db.close()
t=threading.Thread(target=fillWifi_frommysql,args=("../Files/mac.csv",))
t.start()
t.join()



# In[9]:


Datawifi=pd.read_csv("../Files/Wifi.csv",delimiter=",")
Datawifi["subscriber_id"]=Datawifi.subscriber_id.astype(np.str_)
def get_company(x):
    if x[0:2]=="15":
        return "We"
    elif x[0:2]=="11":
        return "Etisalat"
    elif x[0:2]=="10":
        return "Vodafone"
    elif x[0:2]=="12":
        return "Orange"
Datawifi["Company"]=Datawifi.subscriber_id.apply(get_company)


# In[2]:


#Datawifi[Datawifi.subscriber_id=="1064876671"]


# In[3]:


#Datamac[Datamac.subscriber_id=="1064876671"]


# In[4]:


#Datamac.head(1)


# In[10]:


Datamac=pd.read_csv("../Files/mac.csv",delimiter=",")
Datamac["subscriber_id"]=Datamac.subscriber_id.astype(np.str_)


# In[11]:


Datawifi=pd.merge(Datawifi,Datamac,on="subscriber_id",how='outer')


# In[13]:


#Datawifi.drop(["id_x","id_y"])


# In[14]:


htmltxt=""
#Data=pd.read_csv('vasloghourly.csv.wrongData',delimiter='\t')
#Data=pd.read_csv('../Source/mysqlout.csv',encoding='latin-1', engine='c' ,delimiter='\t',low_memory=False) 
Data=pd.read_csv('../Files/vasloghourly.csv',encoding='latin-1', engine='c' ,delimiter=',',low_memory=False
                 )
def ldapnasformat(row):

    return str(row['nas_port_id_ldap'])[15:-1]

###Data['nas_port_id_ldap']=Data['nas_port_id_ldap'].map(lambda x: str(x)[15:-1])



# In[17]:


Datawrongnas=Data[Data['reject_reason']=='Wrong NAS Port Id Or Wrong NAS IP address'].reset_index(drop=True)
uwrongdata=pd.DataFrame(Datawrongnas.user_name.unique())
#uwrongdata=Datawrongnas.user_name.unique()

###uwrongdata=pd.DataFrame(uwrongdata.iloc[2246])
#str(uwrongdata.tolist()).strip()
uwrongdata.columns=["usernames"]
wlist=uwrongdata.usernames.tolist()
Parellel_NAS2.main(wlist,worker_count=20)
nas_results=[(i.username,i.PHnas,i.SVnas) for i in Parellel_NAS2.results if i.PHnas !=i.SVnas and i.SVnas!="unable to connect" and i.PHnas!="unable to connect" ]
uwrongdata=pd.DataFrame.from_records(nas_results)
uwrongdata.columns=[["Username","SV","PH"]]


# In[4]:


domain_u= lambda x:  (x.split("@")[1]) if x.find("@") != -1 else None


# In[5]:


Data["Domain"]=Data.user_name.apply(domain_u)


# In[6]:


#Data.groupby("Domain").size()


# In[7]:


nullData=Data[Data.nas_port_id_request.isnull()]


# In[8]:


#Data.columns


# In[9]:


if len(nullData)> 0:
    nullDatahtml=nullData.to_html()
    htmltxt=htmltxt+nullDatahtml
    


# In[10]:


#nullData=Data[Data.nas_port_id_request.isnull()]


# In[11]:


list1=Data.nas_port_id_request.tolist()


# In[12]:


list2=[]
for i in range(len(list1)):
    try:
        list2.append(list1[i].split('-')[0:-1])
    except:
        list2.append(["Null"])
        #print(list1[i])
            
#'adsl 14 35'.split('-')


# In[13]:


#list3=list2[1:1000]


# In[14]:


n=0
for i in list2:
    if len(i) == 4:
        #print(i)
        del (i[1])
    if len(i) > 3:
        #print(i)
        list2[n]=i[0:3]
    n+=1
#pd.DataFrame(list2)
Datanas_names=pd.DataFrame(list2,columns=['City','Central','provicen'])
#Datanas_names[0:5]
#Data[0:5]


# In[15]:


Data=Data.join(Datanas_names)


# In[16]:


def addpic(imagename,imgstr):
    return """"<div class="header" align="center"> <p>"""+imgstr+ """"<font size="6"></font></p> <img src="cid:"""+imagename[:-4]+""""></div>"""
#addpic('Datagr1.jpg',"Rejection by Server")


# In[17]:


#######################################WIFI################################################

Datagr1=Datawifi.groupby(['Company']).size()

fig, ax = plt.subplots(figsize=(4,4))
explode = (0., .1, 0)  # explode 1st slice
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

pll=Datagr1.plot(kind='pie', ax=ax,autopct='%.02f',colors=colors,fontsize=28)   #g3.head
fig.savefig("Company.jpg",bbox_inches="tight")
Datagr1=pd.DataFrame(Datagr1)
Datagrr=pd.DataFrame(Datagr1)
Datagr1=Datagr1.to_html(classes='pretmlrevew')
Datagrreview=Datagr1
#Datagrreview=Datagr1.to_html(classes='pretmlrevew')
htmltxt=htmltxt+addpic("Company.jpg","Company")+Datagrreview
#htmltxt=htmltxt+addpic("Datagrs.jpg","Rejection and Accept")+Datagr1



Datagr1=Datawifi.groupby(['message_x']).size()

fig, ax = plt.subplots(figsize=(20,4))
explode = (0., .1, 0)  # explode 1st slice
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

pll=Datagr1.plot(kind='bar', ax=ax,color=colors,fontsize=15)   #g3.head
fig.savefig("message.jpg",bbox_inches="tight")
Datagr1=pd.DataFrame(Datagr1)
Datagrr=pd.DataFrame(Datagr1)
Datagr1=Datagr1.to_html(classes='pretmlrevew')
Datagrreview=Datagr1
#Datagrreview=Datagr1.to_html(classes='pretmlrevew')
htmltxt=htmltxt+addpic("message.jpg","message")+Datagrreview
#htmltxt=htmltxt+addpic("Datagrs.jpg","Rejection and Accept")+Datagr1
del(Datawifi)
del(Datagr1)
del()

############################################################################




# In[19]:


len(htmltxt)


# In[20]:




Datagr1=Data.groupby(['status']).size()

fig, ax = plt.subplots(figsize=(4,4))
explode = (0., .1, 0)  # explode 1st slice
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

pll=Datagr1.plot(kind='pie', ax=ax,autopct='%.02f',colors=colors,fontsize=28)   #g3.head
fig.savefig("Datagrs.jpg",bbox_inches="tight")
Datagr1=pd.DataFrame(Datagr1)
Datagrr=pd.DataFrame(Datagr1)
Datagr1=Datagr1.to_html(classes='pretmlrevew')
Datagrreview=Datagr1
#Datagrreview=Datagr1.to_html(classes='pretmlrevew')
htmltxt=htmltxt+addpic("Datagrs.jpg","Rejection and Acceptance")+Datagrreview
#htmltxt=htmltxt+addpic("Datagrs.jpg","Rejection and Accept")+Datagr1


# In[21]:



Datagr1=Data.groupby(['Domain']).size().sort_values(ascending=False)[1:20]

fig, ax = plt.subplots(figsize=(20,4))
explode = (0., .1, 0)  # explode 1st slice
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

pll=Datagr1.plot(kind='bar', ax=ax,color=colors,fontsize=28)   #g3.head
fig.savefig("Domain.jpg",bbox_inches="tight")
Datagr1=pd.DataFrame(Datagr1)
Datagrr=pd.DataFrame(Datagr1)
Datagr1=Datagr1.to_html(classes='pretmlrevew')
Datagrreview=Datagr1
#Datagrreview=Datagr1.to_html(classes='pretmlrevew')
htmltxt=htmltxt+addpic("Domain.jpg","Top 20 Domains")+Datagrreview
#htmltxt=htmltxt+addpic("Datagrs.jpg","Rejection and Accept")+Datagr1


# In[22]:



#Dataprovicen1=Data.groupby(['provicen']).size().sort_values()

# fig, ax = plt.subplots(figsize=(12,4))
# pll=Dataprovicen1.plot(kind='bar', ax=ax,fontsize=20,color=colors)   #g3.head
# fig.savefig("Dataprovicen1.jpg",bbox_inches="tight")
# Dataprovicen1=pd.DataFrame(Dataprovicen1)
# Dataprovicen1.columns=['counts']
# Dataprovicen1.sort_values(by='counts' ,ascending=False)
# Dataprovicen1pic=Dataprovicen1.sort_values(by='counts' ,ascending=False)[0:20]
# #Dataprovicen1.sort_values(by=)
# #Datagrr=      pd.DataFrame(Datagr1)
# Dataprovicen1html=Dataprovicen1.to_html(classes='my_class')
# htmltxt=htmltxt+addpic("Dataprovicen1.jpg","provicen")+Dataprovicen1html



# Servicegroup.columns=['counts']
# Servicegroup=Servicegroup.sort_values(by='counts' ,ascending=False)
#Servicegroupg=Servicegroup.sort_values(by='counts' ,ascending=False)[0:20]



Dataprovicen=Data.groupby(['provicen']).size().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(12,4))
pll=Dataprovicen.plot(kind='bar', fontsize=20, ax=ax,color=colors)   #g3.head
fig.savefig("Dataprovicen.jpg",bbox_inches="tight")

Dataprovicen=pd.DataFrame(Dataprovicen)
Dataprovicen=Dataprovicen.to_html(classes='my_class')
htmltxt=htmltxt+addpic("Dataprovicen.jpg","provicens")+Dataprovicen


###########################################City#############

DataCity=Data.groupby(['City']).size().sort_values(ascending=False)[0:20]
fig, ax = plt.subplots(figsize=(12,4))
pll=DataCity.plot(kind='bar', fontsize=20, ax=ax,color=colors)   #g3.head
fig.savefig("DataCity.jpg",bbox_inches="tight")

DataCity=pd.DataFrame(DataCity)
DataCity=DataCity.to_html(classes='my_class')
htmltxt=htmltxt+addpic("DataCity.jpg","Rejection and Accept  by City")+DataCity


# In[24]:


len(htmltxt)


# In[25]:


DataR=Data[Data.status=='REJECT']
#########################################################Rejection#######
RDataprovicen=DataR.groupby(['provicen']).size().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(12,4))
pll=RDataprovicen.plot(kind='bar', fontsize=20, ax=ax,color=colors)   #g3.head
fig.savefig("DataRprovicen.jpg",bbox_inches="tight")

RDataprovicen=pd.DataFrame(RDataprovicen)
#RDataprovicen
RDataprovicen=RDataprovicen.to_html(classes='my_class')
htmltxt=htmltxt+addpic("DataRprovicen.jpg","TOP Rejection by  provicen")+RDataprovicen
#####################################################By City#############################
DataCity=DataR.groupby(['City']).size().sort_values(ascending=False)[0:20]
fig, ax = plt.subplots(figsize=(12,4))
pll=DataCity.plot(kind='bar', fontsize=20, ax=ax,color=colors)   #g3.head
fig.savefig("DataRCity.jpg",bbox_inches="tight")

DataCity=pd.DataFrame(DataCity)
DataCity=DataCity.to_html(classes='my_class')
htmltxt=htmltxt+addpic("DataRCity.jpg","TOP Rejection by  City")+DataCity


# In[26]:


# Citydf.columns=["count"]
# Citydf=Citydf.sort_values(by="count",ascending=False)
len(htmltxt)


# In[27]:


# Cityhtml=Citydf.to_html(classes='my_class')
# htmltxt=htmltxt+addpic("Dataprovicen1.jpg","provicen")+Cityhtml


# In[28]:



# Datagr1=Data.groupby(['status']).size()/len(Data)*100
# Datagr1=pd.DataFrame(Datagr1)
# prehtml=Datagr1.to_html(classes='pretmlrevew')
# htmltxt=htmltxt+prehtml


# In[29]:


Datagr11=Data.groupby(['reject_reason']).size()
fig, ax = plt.subplots(figsize=(4,4))
pll=Datagr11.plot(kind='pie', ax=ax,autopct='%.2f',colors=colors)   #g3.head
fig.savefig("Datagr11.jpg",bbox_inches="tight")

Datagr11=pd.DataFrame(Datagr11)
Datagr11=Datagr11.to_html(classes='my_class')
#############
Datagr11=Data.groupby(['reject_reason']).size()
fig, ax = plt.subplots(figsize=(12,4))
pll=Datagr11.plot(kind='bar', ax=ax,color=colors)   #g3.head
fig.savefig("Datagr11bar.jpg",bbox_inches="tight")

Datagr11=pd.DataFrame(Datagr11)
Datagr11=Datagr11.to_html(classes='my_class')


########
htmltxt=htmltxt+addpic("Datagr11.jpg","Rejection and Accept  by Server and reason")
htmltxt=htmltxt+addpic("Datagr11bar.jpg","Rejection and Accept  by Server and reason")+Datagr11
#Datagr2

#print(txt)


# In[30]:


Datagr1=Data.groupby(['host_name','status']).size()
fig, ax = plt.subplots(figsize=(12,4))
pll=Datagr1.plot(kind='bar', ax=ax,fontsize=20,color=colors)   #g3.head
fig.savefig("Datagr1.jpg",bbox_inches="tight")
Datagr1=pd.DataFrame(Datagr1)
Datagrr=pd.DataFrame(Datagr1)
Datagr1=Datagr1.to_html(classes='my_class')
htmltxt=htmltxt+addpic("Datagr1.jpg","Rejection and Accept  by Server")+Datagr1


# In[31]:


#Data=Data.style.highlight_null()
#html = Datagrr.style.background_gradient(cmap='viridis', low=.5)
#s=Datagrr.style.highlight_null().render()
#html = Datagrr.style.highlight_null()

#htmltxt=htmltxt+str(html)
#df = df.applymap(config.format_money) -- Doesn't work
#html = s.render()
#Data
len(htmltxt)


# In[32]:


Datagr2=Data.groupby(['reject_reason','host_name']).size()
fig, ax = plt.subplots(figsize=(4,4))
pll=Datagr2.plot(kind='pie', ax=ax,autopct='%.2f',colors=colors)   #g3.head
fig.savefig("Datagr2.jpg",bbox_inches="tight")

Datagr2=pd.DataFrame(Datagr2)
Datagr2=Datagr2.to_html(classes='my_class')
#############
Datagr2=Data.groupby(['reject_reason','host_name']).size()
fig, ax = plt.subplots(figsize=(12,4))
pll=Datagr2.plot(kind='bar', ax=ax,color=colors)   #g3.head
fig.savefig("Datagr2bar.jpg",bbox_inches="tight")

Datagr2=pd.DataFrame(Datagr2)
Datagr2=Datagr2.to_html(classes='my_class')

########
htmltxt=htmltxt+addpic("Datagr2.jpg","Rejection and Accept  by Server and reason")
htmltxt=htmltxt+addpic("Datagr2bar.jpg","Rejection and Accept  by Server and reason")+Datagr2
#Datagr2

#print(txt)


# In[33]:



len(htmltxt)
#Data=Data[0:10]
#Data


# In[34]:


#Data
#s.render()


# In[35]:


#Datac.to_tml('testcss1.html')


# In[36]:


Datagr3=Data.groupby(['nas_ipaddress','host_name']).size().sort_values(ascending=False)[0:10]
fig, ax = plt.subplots(figsize=(12,4))
pll=Datagr3.plot(kind='bar', ax=ax,color=colors)   #g3.head
fig.savefig("Datagr3.jpg",bbox_inches="tight")

Datagr3=pd.DataFrame(Datagr3)
Datagr3=Datagr3.to_html(classes='my_class')
htmltxt=htmltxt+addpic("Datagr3.jpg","Rejection and Accept  by Server and IP")+Datagr3


# In[37]:


Servicegroup=Data.groupby(['service_name']).size()
Servicegroup=pd.DataFrame(Servicegroup)
Servicegroup.columns=['counts']
Servicegroup=Servicegroup.sort_values(by='counts' ,ascending=False)
Servicegroupg=Servicegroup.sort_values(by='counts' ,ascending=False)[0:20]
fig, ax = plt.subplots(figsize=(12,4))
pll=Servicegroupg.plot( kind='bar',ax=ax)   #g3.head
fig.savefig("Servicegroup.jpg",bbox_inches="tight")

Servicegrouphtml=Servicegroup.to_html(classes='my_class')

########
htmltxt=htmltxt+addpic("Servicegroup.jpg","Count Top 30 Services")+Servicegrouphtml
htmltxt=htmltxt+addpic("Datagr2bar.jpg","Rejection and Accept  by Server and reason")
#Datagr2

#print(txt)
#Servicegroup.to_csv('services.csv')


# In[36]:


#Servicegroup.query("service_name == 'eg'")


# In[37]:


#Data.query("service_name == 'eg'")


# In[38]:


#####WIFI Services###################################


len(htmltxt)


# In[39]:



#Servicegroup.sort_values(by='Service_name')


# In[40]:


#Servicegroup


# In[41]:


AData=Data[Data['status']== 'ACCEPT']

# def findfraud(AData):
#     DiffNASData=AData.query('(nas_port_id_ldap!=nas_port_id_request)&nas_port_id_request !=\'null\'')   

#     if DiffNASData.size >0:
#         return 1
#     else:
#         return 0
# if findfraud(AData):
#     ADatahtml=AData.to_html(classes='my_class')
#     htmltxt=htmltxt+ADatahtml
fraudData=AData[["user_name","nas_port_id_request"]].drop_duplicates().groupby("user_name").size().sort_values(ascending=False)

fraudData=pd.DataFrame(fraudData)
fraudData.columns=['counts']
fraudData=fraudData[fraudData.counts>2]
#len(fraudData)
if len(fraudData)>0:
    fraudData=fraudData.to_html(classes='my_class')
    htmltxt=htmltxt+fraudData


# In[44]:


len(htmltxt)


# In[43]:


#htmltxt=""
TOPACCEPT=AData.groupby(['user_name','status'])['nas_port_id_ldap']
TOPACCEPT=pd.DataFrame(TOPACCEPT.count().sort_values(ascending=False)[0:20])
TOPACCEPT.columns=["COUNT ACCEPT "]
TOPACCEPThtml=TOPACCEPT.to_html(classes='my_class')
htmltxt=htmltxt+TOPACCEPThtml


# In[45]:


# #TOPACCEPT100=TOPACCEPT[TOPACCEPT['COUNT ACCEPT' > 100]]
# #TOPACCEPT=TOPACCEPT.astype(int)
# #TOPACCEPT['COUNT ACCEPT ']=TOPACCEPT['COUNT ACCEPT '].apply(int)
# TOPACCEPTc=AData.groupby(['user_name','status'])['nas_port_id_ldap'].count()

# TOPACCEPTc.sort_values(inplace=True)
# TOPACCEPTc=pd.DataFrame(TOPACCEPTc)
# TOPACCEPTc=TOPACCEPTc[TOPACCEPTc.nas_port_id_ldap > 100]
# TOPACCEPTc.to_csv('to-Cisco.csv')
# #TOPACCEPT.columns
# #TOPACCEPT.query('"COUNT ACCEPT "== "100"')


# In[46]:


#TOPACCEPT


# In[45]:


TOPAUTH=Data.groupby(['user_name','status'])['nas_port_id_ldap']
TOPAUTH=pd.DataFrame(TOPAUTH.count().sort_values(ascending=False)[0:20])
#TOPAUTH.count().sort_values(ascending=False)[0:20]
TOPAUTH.columns=["COUNT ALL"]
TOPAUTHhtml=TOPAUTH.to_html(classes='my_class')
htmltxt=htmltxt+TOPAUTHhtml


# In[46]:


Datanoservice=Data[Data['reject_reason']== 'No Service Was Found']
Datanoserviceh=Datanoservice.to_html(classes='my_class')
content =  str.encode(Datanoserviceh)

#Data.groupby("reject_reason").count()
#Datanoservice


# In[49]:


#Datanoservice.user_name.unique()
len(htmltxt)


# In[48]:


Data=Data[Data['status']== 'REJECT']
Datagrreject_reason=Data.groupby(['reject_reason','user_name','host_name',
                                   'nas_port_id_ldap','nas_port_id_request'])['user_name'].size()
#Datagrreject_reason=Data.groupby(['reject_reason'])
#Datagrreject_reason.groups('')
#Datagrreject_reason.groups('Wrong NAS Port Id Or Wrong NAS IP address')
#Datagrreject_reason=Datagrreject_reason.get_group('Wrong NAS Port Id Or Wrong NAS IP address')
#Datagrreject_reason=Datagrreject_reason['host_name','user_name','nas_port_id_ldap','nas_port_id_request']
Datagrreject_reason=pd.DataFrame(Datagrreject_reason)

#Datagrreject_reason['ldap']=Datagrreject_reason.apply(lambda row: row['nas_port_id_ldap'],axis=1)
#Datagrreject_reason=Datagrreject_reason.to_html()
# fig, ax = plt.subplots(figsize=(17,5))
# pll=Datagr3.plot(kind='bar', ax=ax)   #g3.head
# fig.savefig("reject_reason.jpg",bbox_inches="tight")

#Datagrreject_reason=pd.DataFrame(Datagrreject_reason)

#######
# html = Datagrr.style.background_gradient(cmap='viridis', low=.5)
# s=Datagrreject_reason.style.highlight_null().render()
# html = Datagrreject_reason.style.highlight_null()

# htmltxt=htmltxt+str(html)

###

Datagrreject_reason=Datagrreject_reason.to_html(classes='my_class')
#Datagrreject_reason=Datagrreject_reason+AUTHH
content = content + str.encode(Datagrreject_reason)
#content
with gzip.open('REJECT.html.gz', 'wb') as f:
     f.write(content)
#htmltxt=htmltxt+Datagrreject_reason


# In[51]:





# In[52]:


# wrog_nslst=list(Datawrongnas.user_name.unique())
# SVlist=Parellel_NAS.getlistnas('SV',wrog_nslst,500)
#len(htmltxt)


# In[53]:


#PHlist=Parellel_NAS.getlistnas('PH',wrog_nslst,500)    
#333333


# In[54]:


# for ps in Parellel_NAS.processes:
#     print(ps)
#     ps.terminate()


# In[55]:


#r=[Parellel_NAS.compare_stes(SVlist,PHlist)]


# In[56]:


#PHlistt=PHlist[len(PHlist)-732]
#'STOP' in PHlistt
#####pwrongdata['user_ame']=pd.DataFrame(wrog_nslst)


# In[57]:


#PHlistt=PHlist[0:len(PHlist)-732]
#len(PHlistt)

#PHlist[0]
# PHlist = [x for x in PHlist if x != 'STOP']

# pht=pd.DataFrame(list(PHlist),dtype=str)
# pht.columns=('user_name','PH_NAS_ID')

#pht


# In[58]:


#SVlistt=SVlist[0:5]
#SVlistt
# SVlist = [x for x in SVlist if x != 'STOP']

# svt=pd.DataFrame(SVlist)
# svt.columns=('user_name','SV_NAS_ID')
# #svt


# In[59]:


# allt=pd.merge(svt,pht)
# allt['Match']=allt.apply(lambda x: x['PH_NAS_ID']==x['SV_NAS_ID'],axis=1)
# uwrongdata=allt[allt['Match']==False].reset_index(drop=True)
# uwrongdata


# In[60]:


# #
#uwrongdata.columns=['0']
# #ldap_nas_id.comparesites(x[0]),axis=1)
# uwrongdata=uwrongdata.apply(lambda x: str(x[0]).strip(),axis=1)
# #uwrongdata=pd.DataFrame(uwrongdata)


#Datawrongnas=Data[Data['reject_reason']=='Wrong NAS Port Id Or Wrong NAS IP address'].reset_index(drop=True)
#uwrongdata=pd.DataFrame(Datawrongnas.user_name.unique())
#uwrongdata=uwrongdata[0:140]

#testdata=uwrongdata[1000:1010]


# In[61]:


###############################Threading####################################
# uwrongdata.columns=['user_name']
# ll1=uwrongdata.user_name.tolist()
# uwrongdata.user_name.to_pickle('pickle1')
# #ll1=ll1[0:500]
# for i in ll1:
#     ldap_nas_id.filldicts(i)
# len(ldap_nas_id.PHdict)


# In[62]:


#ll1


# In[63]:


#len(ll1)
# uwrongdata=uwrongdata[:2]
# uwrongdata


# In[64]:




# ####uwrongdata['Matchdetals']=uwrongdata.apply(lambda x: ldap_nas_id.comparesites((x[0])),axis=1)
# uwrongdata['Matchdetals']=uwrongdata.apply(lambda x: ldap_nas_id.comparesites((x[0])),axis=1)
# #uwrongdata['Matchdetals']=uwrongdata.apply(lambda x: ldap_nas_id.comparesites('645970@tedata.net.eg\t'),axis=1)
# #testdata
# uwrongdata.columns=['user_name','Matchdetals']
# #uwrongdata


# In[65]:


#len(u[1])


# In[66]:


# %%time
# testdata
#ldap_nas_id.g1("d",[])


# In[67]:


#testdata=testdata['0']
#testdata.apply(lambda x: ldap_nas_id.g1(x),axis=0)


# In[68]:


# uwrongdata['Match']=uwrongdata['Matchdetals'].apply(lambda x: x)
# uwrongdata['Match']=uwrongdata['Match'].apply(lambda x: x[:][0])
# uwrongdata['SV']=uwrongdata['Matchdetals'].apply(lambda x: x[:][1])
# uwrongdata['PH']=uwrongdata['Matchdetals'].apply(lambda x: x[:][2])

# uwrongdata=uwrongdata[uwrongdata['Match']==False].reset_index(drop=True)
# #uwrongdata
#     #uwrongdata.set_option('max_colwidth',40)
# uwrongdata=uwrongdata[['user_name','SV','PH','Match']]
# #uwrongdata


# In[54]:



htmltxt=htmltxt+uwrongdata.to_html(classes='my_class')


# In[56]:


#uwrongdata=uwrongdata[0:14]
#
#uwrongdata['Matchdetals']=uwrongdata.apply(lambda x: ldap_nas_id.comparesites(x[0]),axis=1)


# In[57]:


# del(Data)
# del(uwrongdata)
# del(ADATA)
# del(TOPAUTH)
# del(TOPAUTHhtml)
# del(TOPACCEPThtml)
# del(TOPACCEPT)


# In[56]:


with open('../Files/head2.txt' ,'r') as f:
    d2=f.read()
d3=d2+htmltxt
d3 = pynliner.fromString(d3)

recipients=['xx@tedata.net','xxx@tedata.net','xxx@tedata.net']
#recipients=['Mahmoud.iaboelenin@tedata.net']
Pymailer.send_email('Mahmoud.iaboelenin@tedata.net',recipients,
                    'Rejection Last 6 Hour',d3,"Company.jpg","message.jpg",'Datagrs.jpg','Datagr11.jpg',
                    'Datagr11bar.jpg','Datagr1.jpg','Datagr2.jpg','Datagr2bar.jpg',
                    'Datagr3.jpg','Servicegroup.jpg',
                    "DataCity.jpg","Dataprovicen.jpg","DataRprovicen.jpg","DataRCity.jpg",
                    'REJECT.html.gz' )


# In[44]:


# In[55]:


#with open('../Files/d33.html' ,'w') as f:
#    f.write(d3)

