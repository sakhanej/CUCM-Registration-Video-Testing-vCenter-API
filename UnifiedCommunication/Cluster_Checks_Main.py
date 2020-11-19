## Import Libraries
import sys,os
## Libraries to make WSDL Connections
from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
from zeep.helpers import serialize_object
from requests import Session,request
from requests.auth import HTTPBasicAuth
from lxml import etree
import urllib3,getpass
## Libraries for MultiThreading
import threading
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
## Libraries for Data Processing
from pandas import DataFrame, ExcelWriter,merge,read_excel
from bs4 import BeautifulSoup
import time,datetime,re,math
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3


requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CustomTransport(Transport):
    def load(self, url):
        # Custom URL overriding to local file storage
        if url and url == "http://schemas.xmlsoap.org/soap/encoding/":
            url = "Files/ServSoapSchema.xsd"
        # Call zeep.transports.Transport's load()
        return super(CustomTransport, self).load(url)

class UCNode():
    '''
    This class creates each node as an object 
    '''
    def __init__(self,hostname):
        self.name=hostname
        self.services=DataFrame() #DataFrame with Services Data
        self.ldap=''

class Cluster():
    ''' Global Variables of this class
    Input : Publisher IP Address , AXL Username , AXL Password
    '''
    Ipaddress=""
    axluser=""
    axlpass=""
    reg_data_frame=DataFrame()
    devicedataframe=DataFrame(columns=['DeviceName','Model','DeviceClass','DevicePool'])
    phone_reg_data=DataFrame() ## this dataFrame Contains the registration report for Phones
    ## other devices registration 
    '''Method used to create AXL connection with the Node'''
    @staticmethod
    def setupaxlconnection(self):
        axlwsdl = 'file://'+os.getcwd()+'//Files//AXLAPI.wsdl'
        AXL_BINDING_NAME = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"
        ADDRESS = "https://"+self.Ipaddress+":8443/axl/"
        ## setup Session 
        session = Session()
        session.verify = False
        session.auth = HTTPBasicAuth(self.axluser, self.axlpass)
        transport = CustomTransport(cache=SqliteCache(), session=session, timeout=60)
        history = HistoryPlugin()
        ## Setup Client Connection
        client = Client(wsdl=axlwsdl, transport=transport, plugins=[history])
        axl = client.create_service(AXL_BINDING_NAME, ADDRESS)
        return axl

    '''Method Used to execute SQL
        This method first makes AXL connection and then execute sql query
    '''
    @staticmethod
    def executesql(self,sql):
        try:
            axlservice=self.setupaxlconnection(self)
        except (Fault,Exception) as error:
            print ("Error in SettingAXLConnection ,Verify Credentials \n" + error)
        if axlservice:
            QueryResult=axlservice.executeSQLQuery(sql=sql)
            if QueryResult:
                return QueryResult
            else:
                return None

    '''Method used to fetch all nodes present in the cluster'''
    @staticmethod
    def fetchnodes(self):
        listofnodes=[]
        try:
            sql="select name from processnode where systemnode=='f' and isactive=='t'"
            listofnodes=self.executesql(self,sql)
        except (Fault,Exception) as error:
            print ("Error Fetching Nodes \n"+ str(error))
        return listofnodes

    '''Method to Create a New Publisher Object'''
    def __init__(self,PublisherIP,AXLUsername,AXLPassword):
        self.Ipaddress=PublisherIP ## Publisher IP address
        self.axluser=AXLUsername ## Axl Login to the Publisher
        self.axlpass=AXLPassword ## Axl Login to the Publisher
        self.nodedict={} ## dictionary of all the nodes belonging to this cluster
        try:
            fetchresult=self.fetchnodes(self)
        except (Fault,Exception) as error:
            print (error)
            sys.exit()
        try:
            if fetchresult:
                for dev in fetchresult['return']['row']:
                    self.nodedict[dev[0].text]=UCNode(dev[0].text)
        except:
            print ("Could Not Parse Node Fetch result, Setting only 1 node ie Publisher")
    

    ## Code for Fetching Services
    def setupserviceconnection(self,ip):
        #print (threading.currentThread().getName())
        ## setup Session 
        session = Session()
        session.verify = False
        session.auth = HTTPBasicAuth(self.axluser, self.axlpass)
        transport = CustomTransport(cache=SqliteCache(), session=session, timeout=60)
        history = HistoryPlugin()
        # import required WSDL's
        servicewsdl='file://'+os.getcwd()+'//Files//ServiceWSDL.wsdl'
        SERVICE_BINDING_NAME = "{http://cisco.com/ccm/serviceability/soap/ControlCenterServices/}ControlCenterServicesBinding"
        SERVICE_ADDR="https://"+ip+":8443/controlcenterservice/services/ControlCenterServicesPort"
        try:
            print ("Fetching Services Status from "+ip)
            client = Client(wsdl=servicewsdl, transport=transport, plugins=[history])
            Servicexl = client.create_service(SERVICE_BINDING_NAME,SERVICE_ADDR)
            result=Servicexl.soapGetServiceStatus([''])
            return result
        except (Fault,Exception) as error:
            print (error)
            return None

    def fetchservices(self):
        #Creating a Multi thread pool to fetch services from each node simultaneously
        services_thread_pool = ThreadPoolExecutor(max_workers=8)
        allServicesresults={keys: services_thread_pool.submit(self.setupserviceconnection,keys) for keys in self.nodedict.keys()}
        for node,services in allServicesresults.items():
            #changing datatype to List from zeep object type
            try:
                temp_zeep_service_list=list(services.result()['ServiceInfoList'])
                temp_services=[serialize_object(value) for value in temp_zeep_service_list]
                temp_df=DataFrame.from_dict(temp_services,orient='columns')
                temp_df['ReasonCodeString']=temp_df['ReasonCodeString'].fillna('Activiated',inplace=True)
                #temp_df.drop('ReasonCode',axis=1,inplace=True)
                self.nodedict[node].services=temp_df
            except:
                self.nodedict[node].services="Cannot Find Services"
        return None
    

    ##Code for device Registration
    def getregisteration(self,macs,transport,history):
        ## setup Session 
        # import required WSDL's
        riswsdl='https://'+self.Ipaddress+':8443/realtimeservice2/services/RISService70?wsdl'
        try:
            client = Client(wsdl=riswsdl, transport=transport, plugins=[history])
            RIS_BINDING = "{http://schemas.cisco.com/ast/soap}RisBinding"
            RIS_ADDR = 'https://'+self.Ipaddress+':8443/realtimeservice2/services/RISService70?wsdl'
            risAxl = client.create_service(RIS_BINDING,RIS_ADDR)
            factory = client.type_factory('ns0')
            item=[]
            for mac in macs:
                item.append(factory.SelectItem(Item=mac))
            Item = factory.ArrayOfSelectItem(item)
            stateInfo = ''
            criteria = factory.CmSelectionCriteria(MaxReturnedDevices = 1000,Status='Any',NodeName='',SelectBy='Name',SelectItems=Item)
            result = risAxl.selectCmDevice(stateInfo, criteria)
            return result
        except (Fault,Exception) as error:
            print ("Error in getting RIS report from publisher\n"+ error)
            return None



    def parsedeviceaxl(self,axl_result):
        if axl_result['return']!=None:
            for dev_detail in axl_result['return']['row']:
                self.devicedataframe=self.devicedataframe.append({'DeviceName' : dev_detail[0].text , 'Model' : dev_detail[1].text,'DeviceClass':dev_detail[2].text,'DevicePool': dev_detail[3].text} , ignore_index=True)

    def AXLSQLBreaker(self,sql,total,chunk):
        runtimes=math.ceil(total/chunk)
        for i in range(0,int(runtimes)+1):
            if i==0:
                out=self.phone_execute_axl("select first "+str(chunk)+sql)
                if out=="okay":
                    continue
                else:
                    print(out)
                    break
            else:
                out=self.phone_execute_axl("select skip "+str(chunk*i)+" first "+str(chunk)+sql)
                if out=="okay":
                    continue
                else:
                    print(out)
                    break

    def phone_execute_axl(self,sql):
        try:
            axlservice=self.setupaxlconnection(self)
        except (Fault,Exception) as error:
            print ("Error in Setting AXL Connection for Devices \n" + str(error))
        if axlservice:
            try:
                QueryResult=axlservice.executeSQLQuery(sql=sql)
                self.parsedeviceaxl(QueryResult)
                return "okay"
            except (Fault,Exception) as error:
                return str(error)


    def fetchdevicesAXL(self):
        devicesql=" d.name as DeviceName, tm.name as Model ,tc.name as DeviceClass ,dp.name as Devicepool from device as d left join typemodel as tm on d.tkmodel=tm.enum left join typeclass as tc on tc.enum=d.tkclass left join devicepool as dp on d.fkdevicepool=dp.pkid where d.tkclass in (1,2,4,5,12,18,19) and d.tkmodel!=645 order by DeviceName"
        axl_devices=self.phone_execute_axl("select"+devicesql)
        if axl_devices=="okay":
            print ("Devices list fetched from CUCM, running Registration checks")
            return None
        else:
            print (axl_devices)
            z=re.search(r'Total[\s\S]+:\s?(\d+)[\s\S]+less\s?than\s?(\d+)\s?rows',axl_devices)
            if z:
                print ("DeviceCount is high!! This report might take  more time")
                self.AXLSQLBreaker(devicesql,int(z.group(1)),int(z.group(2)))
            else:
                print ("Error Fetching DeviceList")
                sys.exit()

    @staticmethod
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def parse_reg_result(self,register_report):
        #print (register_report)
        for noderesult in register_report['SelectCmDeviceResult']['CmNodes']['item']:
            if noderesult['ReturnCode']=='Ok':
                node=noderesult['Name']
                CmDevices=noderesult['CmDevices']['item']
                for phones in CmDevices:
                    #print (phones['IPAddress'])
                    if phones['IPAddress']!=None:
                        self.reg_data_frame=self.reg_data_frame.append({'DeviceClass':phones['DeviceClass'],'DeviceName': phones['Name'],'node':node,'Protocol':phones['Protocol'],'Status':phones['Status'],'desc':phones['Description'],'Aload':phones['ActiveLoadID'],'Inload':phones['InactiveLoadID'],'DirectoryNumber':phones['DirNumber'],'IPAddress':phones['IPAddress']['item'][0]['IP'],'LoginUserId':phones['LoginUserId'],'TimeStamp':time.strftime("%d %b %Y %H:%M:%S %Z", time.localtime(phones['TimeStamp']))}, ignore_index=True)
                    else:
                        self.reg_data_frame=self.reg_data_frame.append({'DeviceClass':phones['DeviceClass'],'DeviceName': phones['Name'],'node':node,'Protocol':phones['Protocol'],'Status':phones['Status'],'desc':phones['Description'],'Aload':phones['ActiveLoadID'],'Inload':phones['InactiveLoadID'],'DirectoryNumber':phones['DirNumber'],'IPAddress':"Not Found",'LoginUserId':phones['LoginUserId'],'TimeStamp':time.strftime("%d %b %Y %H:%M:%S %Z", time.localtime(phones['TimeStamp']))}, ignore_index=True)
                         
    @staticmethod
    def RegistrationReportprocessing(self):
        #devicedataframe  : This DF is for  device details from AXL
        #reg_data_frame : This DF is for Registration from Ris
        phone_reg=self.reg_data_frame[self.reg_data_frame.DeviceClass=='Phone']
        phones=self.devicedataframe[self.devicedataframe.DeviceClass=='Phone']
        ## code to generate Phone Registration Report
        phone_reg.sort_values(['DeviceName','TimeStamp','Status'],inplace=True,ascending=[True,False,True])
        phone_reg.reset_index(inplace=True)
        phone_reg.insert(3,'DuplicateCheck',phone_reg.duplicated(subset='DeviceName',keep='first'),allow_duplicates=True)
        phone_reg.drop(phone_reg[phone_reg.DuplicateCheck==True].index,inplace=True)
        phone_reg.drop('DuplicateCheck',axis=1,inplace=True)
        Phone_Registration=merge(left=phones,right=phone_reg,left_on='DeviceName',right_on='DeviceName',how='left')
        self.phone_reg_data=Phone_Registration.loc[:,['DeviceName','desc','Status','Model','DevicePool','Aload','DirectoryNumber','IPAddress','Inload','node','Protocol','LoginUserId','TimeStamp']]

    def fetchregistrationdata(self):
        
        try:
            self.fetchdevicesAXL() ## fetch deviceList from AXL
            #print ("DeviceList Fetch!! getting Registration Report")
            hostname=list(self.devicedataframe['DeviceName'])
            chunked_hostname_list=list(self.chunks(hostname,800))
            ## Setup Session with the Publisher
            session = Session()
            session.verify = False
            session.auth = HTTPBasicAuth(self.axluser, self.axlpass)
            transport = CustomTransport(cache=SqliteCache(), session=session, timeout=60)
            history = HistoryPlugin()
            print ("Total Connections for registration "+str(len(chunked_hostname_list)))
            i=1
            for mac_list in chunked_hostname_list:
                try:
                    print ("Connection "+ str(i))
                    reg_result=self.getregisteration(mac_list,transport,history)
                    i=i+1
                    try:
                        self.parse_reg_result(reg_result)
                    except(Fault,Exception) as error:
                        print ("Cannot Parse Returned Registration Report \n "+ str(error))
                except(Fault,Exception) as error:
                    print ("Cannot fetch Registration Report \n "+ str(error))
            try:
                self.RegistrationReportprocessing(self)
            except (Fault,Exception) as error:
                print ("Error Compiling Registration Report !! Returning Raw Report\n")
                print (error)
        except:
            print ("Error fetching Registration Report in main function")
            sys.exit()
        
        
        
    @staticmethod
    def multildapconnection(ip,username,password):
        #print (threading.currentThread().getName())
        url = "https://"+ip+"/ccmadmin/j_security_check"
        querystring = {"appNav":"ccmadmin","j_username":username,"j_password":password}
        payload = ""
        headers = {'Host': ip,'Origin': "https://"+ip,'Content-Type': "application/x-www-form-urlencoded",'Referer': "https://"+ip+"/ccmadmin/index.jsp",'cache-control': "no-cache"}
        try:
            response = request("POST", url, data=payload, headers=headers, params=querystring,verify=False)
            if response:
                soup=BeautifulSoup(response.text,features="lxml")
                message = soup.findAll("fieldset")
                if message:
                    return (message[0].text+" on "+ip)
                else:
                    return ("Login Working on Node: "+ip)
        except (Fault,Exception) as error:
            print (error +" on "+ ip)
            return ("Error setting connection on "+ip)


    def checkldap(self):
        username=input("Enter Username to check Login: ")
        password = getpass.getpass('Enter Password : ')
        ldap_thread_pool = ThreadPoolExecutor(max_workers=10) 
        try:
            allldapResults={keys: ldap_thread_pool.submit(self.multildapconnection,keys,username,password) for keys in self.nodedict.keys()}
            for node,ldap in allldapResults.items():
                self.nodedict[node].ldap=str(ldap.result())
        except:
            print ("Error Checking Login on each node")
