from Cluster_Checks_Main import Cluster
import urllib3,getpass,gc,time,datetime,re,math


## disable URL warning if needed

ipaddress=input("Enter Publisher IPAddress/Hostname : ")
username=input("Enter Username: ")
auth = getpass.getpass('Enter Password : ')

## Actual Code

## Create a Cluster Object 
firstnode=Cluster(ipaddress,username,auth)

## As part of this object creation, all cluster nodes are fetched
## can be assess through

## A dictionary is returned with key as all nodes in this cluster
print (firstnode.nodedict.keys())
# firstnode.fetchservices()
# for key in firstnode.nodedict.keys():
#     print (firstnode.nodedict[key].services)

firstnode.checkldap()
for key in firstnode.nodedict.keys():
    print (firstnode.nodedict[key].ldap)
# firstnode.fetchregistrationdata()
# print (firstnode.phone_reg_data)
'''
1. To check the services status on nodes in this cluster
firstnode.fetchservices()

Results are fetched and stored in nodedict.services as dataframe, can be returned as 
firstnode.nodedict[key].services [ DataFrame retunred]

2. Registration report can be fetched using 
firstnode.fetchregistrationdata()

#devicedataframe  : This DF is for  device details from AXL
#reg_data_frame : This DF is for Registration from Ris
# phone_reg_data : Compiled Registration Report for Phones


3. lDap checks can be called and checked as:

    firstnode.checkldap()
    results can be viewed as :
    firstnode.nodedict[key].ldap [ Str returned]
# timestr = time.strftime("%Y%m%d-%H%M%S")

# ## fetchservices from CUCM Clusters
# userinput=input('1. All Services Status \n2. Phone Registration\n3. LDAP Checks\n')
# #userinput=2 ## remove this at last
# if (int(userinput)==1):
#     firstnode.fetchservices() # result can be printed in the form '

#     with ExcelWriter('ServicesOutput.xlsx') as writer:
#         for key in firstnode.nodedict.keys():
#             try:
#                 firstnode.nodedict[key].services.to_excel(writer, sheet_name=key,index=False)
#             except:
#                 print ("Cannot Fetch Services from Node \t"+ key)


# elif (int(userinput)==2):
#     phone_report=firstnode.fetchregistrationdata()
#     #firstnode.devicedataframe.to_excel("deviceframe.xlsx",index=False,sheet_name="Registration Report")
#     firstnode.phone_reg_data.to_excel("Registration Report_"+ipaddress+"_"+timestr+".xlsx",index=False,sheet_name="Phone Registration Report")

# elif(int(userinput)==3):
#     firstnode.checkldap()'''