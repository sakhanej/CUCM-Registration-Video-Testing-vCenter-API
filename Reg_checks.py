from Cluster_Checks_Main import Cluster
import getpass,sys
from Firmwareanalysis import perform_analysis, write_analysis_to_excel_pandas
import json,time
from pandas import ExcelWriter
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3


requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def inputfunction():
    userinput=6
    while int(userinput)>5:
        userinput=input('1. All Services Status \n2. Phone Registration \n3. Phone Firmware Analysis\n 4. Ldap Checks\n 5. Exit\nSelect  option (1-5) : ')
    return int(userinput)

def main(selection,firstnode):
    if (selection==1):
        firstnode.fetchservices()
        timestr = time.strftime("%Y%m%d-%H%M%S")
        with ExcelWriter('ServicesOutput_'+firstnode.Ipaddress+'_'+timestr+'.xlsx') as writer:
            for key in firstnode.nodedict.keys():
                try:
                    firstnode.nodedict[key].services.to_excel(writer, sheet_name=key,index=False)
                except:
                    print ("Cannot Fetch Services from Node \t"+ key)
    elif (selection==2):
        try:
            firstnode.fetchregistrationdata()
            timestr = time.strftime("%Y%m%d-%H%M%S")
            firstnode.phone_reg_data.to_excel("Registration_Report_"+firstnode.Ipaddress+'_'+timestr+".xlsx",index=False,sheet_name="Registration Report")
        except:
            print ("Could not fetch registration report")
    elif (selection==3):
        firstnode.fetchregistrationdata()
        print ("Registration Report fetched")
        firmwaredf=firstnode.phone_reg_data[['DeviceName','Status','Model','Aload']]
        firmwaredf.Aload=firmwaredf.Aload.fillna(value='blank')
        timestr = time.strftime("%Y%m%d-%H%M%S")
        analysis = perform_analysis(firmwaredf)
        #print(json.dumps(analysis, sort_keys=True, indent=4))
        firmwarereport_df=write_analysis_to_excel_pandas(analysis)        
        writer = ExcelWriter('Firmware_Analysis_'+firstnode.Ipaddress+'_'+timestr+'.xlsx', engine='xlsxwriter')
        firmwarereport_df.to_excel(writer, sheet_name='FW Analysis')
        firstnode.phone_reg_data.to_excel(writer,index=False, sheet_name="Registration Report")
        writer.save()
    elif (selection==4):
        try:
            firstnode.checkldap()
            for key in firstnode.nodedict.keys():
                print (firstnode.nodedict[key].ldap)
        except:
            print ("could not do Ldap checks")
    else:
        pass

    recur=input("Type \"yes\" to Continue, Return to Exit : ")
    return recur

if __name__ == '__main__':
    recursion='yes'
    ipaddress=input("Enter Publisher IPAddress/Hostname : ")
    username=input("Enter Username: ")
    auth = getpass.getpass('Enter Password : ')
    print ("\nFetching All Nodes in this Cluster")
    firstnode=Cluster(ipaddress,username,auth)
    while recursion=='yes':
        option=inputfunction()
        recursion=main(option,firstnode)

