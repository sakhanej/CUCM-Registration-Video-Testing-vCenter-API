from pyVim.connect import SmartConnectNoSSL, Disconnect,SmartConnect
import ssl
import json
from pandas import DataFrame, ExcelWriter
import sys

## use this if have to disable SSL Verification
s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE


try:
    c = SmartConnect(host="vCenter Hostname/IP", user="", pwd='')
    print('Valid certificate')
except:
    c = SmartConnect(host="vCenter Hostname/IP", user="", pwd='', sslContext=s)
    print('Invalid or untrusted certificate')
 

def get_host_details(esxihost):
    esxidetails={}
    datastore_str=''
    network_str=''
    for ds in esxihost.host[0].datastore:
        datastore_str=datastore_str+json.dumps({'Name':ds.name,'total(Gb)':round(int(ds.summary.capacity)/1e+9,2),'free(Gb)':round(int(ds.summary.freeSpace)/1e+9,2),'Used(Gb)':round(round(int(ds.summary.capacity)/1e+9,2)-round(int(ds.summary.freeSpace)/1e+9,2),2)})+'\n'
    for network in esxihost.host[0].network:
        network_str=network_str+network.name+'\n'

    esxidetails={'Esxi_Name':esxihost.name,'Total_CPU_Cores':esxihost.summary.numCpuCores,'Logical_CPU_Core':esxihost.summary.numCpuThreads,'CPU(in GHz)':(int(esxihost.summary.totalCpu)/1000),'Total Memory(in Gb)':(int(esxihost.summary.totalMemory)/1e+9),'UCS_Model':esxihost.host[0].hardware.systemInfo.model,'UCS_Vendor':esxihost.host[0].hardware.systemInfo.vendor,'CIMC_Version':esxihost.host[0].hardware.biosInfo.biosVersion,'Status':esxihost.host[0].runtime.connectionState+' || '+esxihost.host[0].runtime.powerState,'DataStores':datastore_str,'Network(NIC)':network_str}
    esxi_partial_df1=DataFrame(esxidetails,index=[0])
    return esxi_partial_df1



def get_vm_details(esxihost):
    vm_machines=esxihost.host[0].vm
    Esxi_VM_df=DataFrame(columns=['VM_Name','VM_Guest','VM_Guest_Hostname','VM_Guest_IpAddress','VMware_tools_Status','Status','Vmware_tools_Upgrade_Policy','Network','VM_desc','CPU_reservation(MHz)','Total_memory(MB)','No_of_CPU','Memory_reservation(MB)','Storage'])
    for vm in vm_machines:
        storage_str=''
        network_str=''
        for storage in vm.storage.perDatastoreUsage:
            storage_str=storage_str+json.dumps({'Name':storage.datastore.name,'total(Gb)':round(int(storage.committed)/1e+9+int(storage.uncommitted)/1e+9,2),'Used(GB)':round(int(storage.committed)/1e+9,2),'free(GB)':round(int(storage.uncommitted)/1e+9,2)})+'\n'
        for network in vm.network:
            network_str=network_str+network.name+'\n'
        vmdetails={'VM_Name':vm.name,'VM_Guest':vm.config.guestFullName,'VM_Guest_Hostname':vm.summary.guest.hostName,'VM_Guest_IpAddress':vm.summary.guest.ipAddress,'VMware_tools_Status':vm.summary.guest.toolsRunningStatus+" || "+vm.summary.guest.toolsVersionStatus,'Status':vm.runtime.connectionState+" || "+vm.runtime.powerState,'Vmware_tools_Upgrade_Policy':vm.config.tools.toolsUpgradePolicy,'Network':network_str,'VM_desc':vm.config.annotation,'CPU_reservation(MHz)':vm.config.cpuAllocation.reservation,'Total_memory(MB)':vm.config.hardware.memoryMB,'No_of_CPU':vm.config.hardware.numCPU,'Memory_reservation(MB)':vm.config.memoryAllocation.reservation,'Storage':storage_str}
        vm_partial_df1=DataFrame(vmdetails,index=[0])
        Esxi_VM_df=Esxi_VM_df.append(vm_partial_df1,ignore_index=True)

    return Esxi_VM_df



def getdetails(vcenter,**kwargs):
    ''' This function fetches host details and also VM inside each host.
    It operates on 3 modes:
        1. options=0 : fetches all Esxi hosts, all VM's under each Esxi host
        2. options=1 : fetches all Esxi hosts only
        3. options=2 : Fetches all details (VM's and Esxi) based on user input. Provide the list of Esxi hosts to fetch details.
    
    Use attribute "esxilist" to provide list of esxi host. Note: The name should exactly match with what present in vcenter
    '''
    datacenter = vcenter.content.rootFolder.childEntity
    Esxi_df=DataFrame(columns=['Esxi_Name','Total_CPU_Cores','Logical_CPU_Core','CPU(in GHz)','Total Memory(in Gb)','UCS_Model','UCS_Vendor','CIMC_Version','Status','DataStores','Network(NIC)'])
    esxi_vm_dict={}

    if int(kwargs['options'])==0:
        for dc in datacenter:
            hostFolder=dc.hostFolder.childEntity
            ## fetching details for each esxi returing Esxi_df as finalised output
            for esxihost in hostFolder:
                df2=get_host_details(esxihost)
                Esxi_df=Esxi_df.append(df2,ignore_index=True)
            ## fetching VM details from each Esxi host
            for esxihost in hostFolder:
                df3=get_vm_details(esxihost)
                esxi_vm_dict[esxihost.name]=df3

    elif int(kwargs['options'])==1:
        for dc in datacenter:
            hostFolder=dc.hostFolder.childEntity
            ## fetching details for each esxi returing Esxi_df as finalised output
            for esxihost in hostFolder:
                #print (esxihost)
                df2=get_host_details(esxihost)
                Esxi_df=Esxi_df.append(df2,ignore_index=True)

    elif int(kwargs['options'])==2:
        ## checking list of esxi's provided
        if 'esxilist' in kwargs:
            for dc in datacenter:
                hostFolder=dc.hostFolder.childEntity
                ## fetching details for each esxi returing Esxi_df as finalised output
                for esxihost in hostFolder:
                    if esxihost.name in kwargs['esxilist']:
                        df2=get_host_details(esxihost)
                        Esxi_df=Esxi_df.append(df2,ignore_index=True)
                ## fetching VM details from each Esxi host
                for esxihost in hostFolder:
                    if esxihost.name in kwargs['esxilist']:
                        df3=get_vm_details(esxihost)
                        esxi_vm_dict[esxihost.name]=df3
        else:
            print ("Please provide list of esxi's using esxilist attribute of getdetails function")
            sys.exit


    with ExcelWriter('vcenter_details.xlsx') as writer:
        Esxi_df.to_excel(writer,sheet_name='Esxi_Details',index=False)
        for key, value in esxi_vm_dict.items():
            value.to_excel(writer,sheet_name=key,index=False)

getdetails(c,options=0,esxilist=['as-bgl-gdc-esxi-09.cisco.com'])