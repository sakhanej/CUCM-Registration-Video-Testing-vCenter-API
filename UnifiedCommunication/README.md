## Understanding the files
- **Cluster_Checks_Main.py**:
  - Capabilities:
    - This file is an WSDL implementation of CUCM AXL/RIS/Services API and web scrapping for login checks.
    - The code is written into modular approach i.e use of class and objects.
    - RIS WSDL is used to fetch registration report from CUCM nodes. it implements SelectCmDevice method of WSDL.
    - Services WSDL is used to fetch services status from all nodes in the CUCM Cluster.
    - Login checks: Validates login to each node in the cluster through GUI. Uses python web scraping library.
  - Inputs:
    - Create a new folder "Files" in your working repository and copy from files from [SupportFiles](https://github.com/sakhanej/CiscoLive2019/tree/master/UnifiedCommunication/Support%20Files) into that folder.
      - WSDL and XSD files are used for WSDL implementation.
      - Model Firmware Compatibility.xlsx : Used for firmware analysis
  - Outputs:
    - Registration Report (dataframe)
    - Services Status (dataframe)
    - Login working status(string)
    
- **Firmwareanalysis.py**:
  - Capabilities:
    - This file compares firmwares found in registration report against "Model Firmware Compatibility" Excel and generates a report. The report depicts what firmwares are tested by Cisco and what tested by customer.
   - Inputs:
     - uses registration report as dataframe
     - Model Firmware Compatibility.xlsx: copied from SupportFiles folder
   - Outputs:
      - Firmware Analysis Report (dataframe)


## How to use files:
**Methods and Attributes available:**

- Import Cluster Object from this file
   ```from Cluster_Checks_Main import Cluster```

- Create a Cluster Object 
  ```firstnode=Cluster(ipaddress,username,auth)
     #Inputs : Publisher IP address, AXL Username, AXL Password ```

- **Methods Available:**
  - fetchservices() : 
      - Call this method  to fetch services status from all nodes in the cluster. 
      - This uses multithreading techniques threshold to 8 threads.
                  
  - fetchregistrationdata() : 
      - Call this method to fetch phones registration status from the cluster.
      
  - checkldap() : 
      - Call this method to check ldap login on each node of the cluster. 
      - This uses multithreading techniques threahold upto 8 threads.


- **Attributes Available:**
  - firstnode.nodedict : 
     - This returns a dictionary of each node as an object.
  - firstnode.nodedict.keys() : 
      - list of CUCM nodes in the cluster.
  - firstnode.nodedict\[key].services : 
      - This return the dataFrame with services status on the particular node, as mentioned by                                        "key"
  - firstnode.nodedict \[key].ldap : 
       - his returns the string output [ldap worked or not]
  - firstnode.devicedataframe : 
       - This dataframe contains the DeviceList output from AXL 
       - AXL Output Fields : [ DeviceName, DevicePool,DeviceClass,Model ]
  - firstnode.reg_data_frame : 
       - This dataframe return the raw Registration output from CUCM. 
       - This might contains duplicate/extra records.

  - firstnode.phone_reg_data : 
       - This dataframe provide the combined/processed Phone Registration 
       - Report can be used as input to further script logic.


# Reference Code : 
  Cluster_Checks_Reference.py
