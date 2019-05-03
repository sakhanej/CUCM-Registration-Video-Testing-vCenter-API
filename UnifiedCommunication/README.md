
This Document provides an overview on how to use # Cluster_Checks_Main python file

# Overview

The python file is an WSDL implementation of CUCM API's.
1. Registration API [ RIS WSDL ] is used to fetch registration report from CUCM Publisher. This script implements SelectCmDevice method of WSDL.
2. Services API [ Services WSDL ] is used to fetch Services status from different nodes in CUCM Cluster
3. LDAP checks : Validates login to each node in the Cluster through GUI to validate LDAP logins works. This uses webscraping techniques.

# Methods and Attributes available:


## Import Cluster Object from this file
  from Cluster_Checks_Main import Cluster

## Create a Cluster Object 
#### Inputs : Publisher IP address, AXL Username, AXL Password 

  firstnode=Cluster(ipaddress,username,auth) 


## Methods availble

### fetchservices() : 
      Call this method  to fetch services status from all nodes in the cluster. 
      This uses multithreading techniques threshold to 8 threads.
                  
### fetchregistrationdata() : 
      Call this method to fetch phones registration status from the cluster.
      
### checkldap() : 
      Call this method to check ldap login on each node of the cluster. 
      This uses multithreading techniques threahold upto 8 threads.


## Available attributes.

### firstnode.nodedict : 
              This returns a dictionary of each node as an object.
### firstnode.nodedict.keys() : 
              list of CUCM nodes in the cluster.
### firstnode.nodedict[key].services : 
              This return the dataFrame with services status on the particular node, as mentioned by                                        "key"
### firstnode.nodedict[key].ldap : 
              This returns the string output [ ldap worked or not ]

### firstnode.devicedataframe : 
               This dataframe contains the DeviceList output from AXL 
               AXL Output Fields : [ DeviceName, DevicePool,DeviceClass,Model ]

### firstnode.reg_data_frame : 
              This dataframe return the raw Registration output from CUCM. 
              This might contains duplicate/extra records.

### firstnode.phone_reg_data : 
              This dataframe provide the combined/processed Phone Registration 
              Report can be used as input to further script logic.


# Reference Code : 
  Cluster_Checks_Reference.py
