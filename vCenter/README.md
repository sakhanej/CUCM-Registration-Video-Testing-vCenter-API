## Understanding the Script

- It uses python pyvnomi library to setup connection with vCenter/vSpehere.
- Refer **requirements.txt** for compatible version with python 3.7
- it uses Managed Object Browser of vCenter/vSphere.

## Scripts Functions

### Create Connection
  - use following pyVim objects to create connection:
    - **SmartConnect**: This object verifies SSL connection
    - To avoid SSL connection error, using below 2 ways:
      - Use **SmartConnect** with sslContext [ mentioned in code ]
      - Use **SmartConnectNoSSL** object to create connection
      
### Fetch Details from vCenter
   ##### getdetails function:
   - This function accepts 3 inputs:
      - **connection object**: e.g. ```c = SmartConnect(host="vCenter Hostname/IP", user="", pwd='')```
      - **options attribute**: 
        1. options=0: Fetches all Esxi hosts, VM's under each Esxi host
        2. options=1: Fetches all Esxi hosts only
        3. options=2: Fetches all details (VM's and Esxi) based on user input. Provide the list of Esxi hosts to fetch                               details.
      - **esxilist**: This attribute is only valid when options=2.
         - Provide the list of ESXI host for which details are required. E.g below
          ```getdetails(c,options=0,esxilist=['host1','host2'])```
          
   ##### get_vm_details function:
   - This function fetches details for each VM in a particular Esxi Host
   ##### get_host_details function:
   - This function fetches details for each Exsi host present in vCenter
    
### Output
  - Output of this scripts is returned as Esxi Dataframe and ESXI_VM dictionary.
    - Esxi_df: This dataframe contains details about all esxi host in vCenter
    - esxi_vm_dict: This dictionary contains details about all VM present in each Esxi host.
                    key: Esxi host , value: VM details dataFrame
                    
### References:
   - A working script is attached where you can see functions in actions.
   - It returns an excel output with all information based on options attribute
   - Attached script is tested on **vSphere Web Client Version 6.5.0.20000 Build 8307201**

### Future Scope/Versions:
  - **Managed Object Browser (MOB) might change based on vSphere Client version**.
  - Deviation might be found in tree structure of the MOB, Please trace the MoB tree based on code provided and make
    required changes.Structure might depend on number of folders made. 
  - This Script was also tested on **vSphere Web Client Version 6.5.0.20000 Build 10949473** 
    - Following changes were made to particular segment of code:
    ``` for esxihost in hostFolder:
          for esxi in esxihost.childEntity: ## this extra loop was added
               df2=get_host_details(esxi)
               Esxi_df=Esxi_df.append(df2,ignore_index=True)
     ```
   - Above code is to cater one extra depth in MoB Tree Structure.
    
   
