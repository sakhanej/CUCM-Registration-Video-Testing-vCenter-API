from Cluster_Checks_Main import Cluster
import getpass

ipaddress=input("Enter Publisher IPAddress/Hostname : ")
username=input("Enter Username: ")
auth = getpass.getpass('Enter Password : ')

firstnode=Cluster(ipaddress,username,auth)

print (firstnode.nodedict.keys())

firstnode.fetchservices()
for key in firstnode.nodedict.keys():
    print (firstnode.nodedict[key].services)

firstnode.checkldap()
for key in firstnode.nodedict.keys():
    print (firstnode.nodedict[key].ldap)

firstnode.fetchregistrationdata()
print (firstnode.phone_reg_data)
