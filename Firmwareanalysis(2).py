import re, math,os,time
from pandas import DataFrame,read_excel,ExcelWriter
import numpy as np

def perform_analysis(regDF):
    print("Analysing Firmwares based on the Registration Report Generated!")
    df1 = regDF
    #df1 = read_excel(filepath, sheetname='Registration Report')
    df1 = df1.replace(np.nan, '', regex=True)
    certified_fw_df = read_excel(os.getcwd()+'\\Files\\Model Firmware Compatibility.xlsx',sheetname='Customer Certified FW')
    ciscoTested_fw_df = read_excel(os.getcwd()+'\\Files\\Model Firmware Compatibility.xlsx',sheetname='Cisco Tested FW')
    # df1.groupby(['model','RegStatus','ActiveLoadId'])
    # print(df1.head())
    model_types = df1['Model'].unique()
    # print(model_types)
    analysis = dict()
    for model_type in model_types:
        model_analysis = dict()
        provisioned_df = df1.loc[df1['Model'] == model_type]
        # print(provisioned_df)
        if 'TelePresence' in model_type or 'Spark' in model_type:
            model_analysis['Type']='Video Endpoint'
        elif 'Cisco Unified Client Services Framework' in model_type or 'Cisco IP Communicator' in model_type:
            model_analysis['Type'] = 'Soft Phone'
        else:
            model_analysis['Type'] = 'Hard Phone'
        model_analysis['provisioned_devices'] = provisioned_df.shape[0]
        # print(model_type,':\n' ,provisioned_df)
        # print(provisioned_df['RegStatus'])
        registered_df = provisioned_df.loc[provisioned_df['Status'] == 'Registered']
        # print(registered_df)
        certified_fw_s = certified_fw_df.loc[certified_fw_df['Model']==model_type].reset_index(drop=True)
        if not certified_fw_s.empty:
            certified_fw = certified_fw_s.iloc[0]['Firmware']
        else:
            certified_fw = 'Not Present in the Script\'s Database'
        # print(model_type,certified_fw)
        # print(certified_fw_s)
        model_analysis['certified_fw']=certified_fw
        # print("Model :",model_type)
        # print("Certified :",certified_fw)
        tested_model_df = ciscoTested_fw_df.loc[ciscoTested_fw_df['Model'] == model_type]
        if (not tested_model_df.empty):
            tested_firmwares = tested_model_df['Firmware'].str.cat(sep='\n')
        else:
            tested_firmwares = 'Not Present in the Script\'s Database'
        model_analysis['tested_fw'] = tested_firmwares
        # print(tested_firmwares)
        model_analysis['registered_devices'] = registered_df.shape[0]
        firmware_types = registered_df['Aload'].unique()
        # print(firmware_types)
        model_fw_analysis=dict()
        if len(firmware_types)!=0:
            for firmware_type in firmware_types:
                firmware_analysis = dict()
                firmware_df = registered_df.loc[registered_df['Aload'] == firmware_type]
                firmware_analysis['numberofdevices'] = firmware_df.shape[0]
                # print("Firmware :",firmware_type)
                # tested_flag = False
                # certified_flag = False
                if certified_fw == firmware_type:
                    # print('FW is certified')
                    firmware_analysis['compatibilty'] = 'Firmware is Compatible'
                    firmware_analysis['upgraderequired'] = 'No'
                    firmware_analysis['upgradepriority'] = 'NA'
                    firmware_analysis['customer_certified'] = 'Yes'
                    firmware_analysis['cisco_tested'] = 'Yes'
                else:
                    # print(tested_model_df.empty,tested_model_df['Firmware'].str.contains(firmware_type).any())
                    if (not tested_model_df.empty) & (tested_model_df['Firmware'].str.contains(firmware_type).any()):
                        # print('FW is tested')
                        firmware_analysis['compatibilty'] = 'Firmware is Compatible'
                        firmware_analysis['upgradepriority'] = 'P2'
                        firmware_analysis['upgraderequired'] = 'Yes'
                        firmware_analysis['customer_certified'] = 'No'
                        firmware_analysis['cisco_tested'] = 'Yes'
                    else:
                        # print('FW is not tested')
                        firmware_analysis['upgraderequired'] = 'Yes'
                        firmware_analysis['upgradepriority'] = 'P1'
                        firmware_analysis['compatibilty'] = 'Firmware is not Compatible'
                        firmware_analysis['customer_certified'] = 'No'
                        firmware_analysis['cisco_tested'] = 'No'
                model_fw_analysis[firmware_type] = firmware_analysis
                model_analysis['firmware_analysis']=model_fw_analysis
        else:
            model_analysis['firmware_analysis']=""
        analysis[model_type] = model_analysis
    # print(analysis)
    return analysis

def write_analysis_to_excel_pandas(analysis):
    print("Writing Analysis to the Excel!")
    rows = []
    for key,value in analysis.items():
        model =key
        # print(key,value)
        provdevices = str(value['provisioned_devices'])
        regdevices = str(value['registered_devices'])
        certified_fw = str(value['certified_fw'])
        type = str(value['Type'])
        tested_fw = str(value['tested_fw'])
        if value['firmware_analysis']!='':
            for firmware,values in value['firmware_analysis'].items():
                # print(values)
                firmware = str(firmware)
                cisco_tested = str(values['cisco_tested'])
                compatibilty = str(values['compatibilty'])
                customer_certified = str(values['customer_certified'])
                numberofdevices = str(values['numberofdevices'])
                upgradepriority = str(values['upgradepriority'])
                upgraderequired = str(values['upgraderequired'])
                row = [model,provdevices,regdevices,certified_fw,
                    tested_fw,
                    type,
                    firmware,numberofdevices,
                    customer_certified,cisco_tested,compatibilty,
                    upgraderequired,upgradepriority]
                rows.append(row)
        else:
            firmware = ''
            cisco_tested = ''
            compatibilty = ''
            customer_certified = ''
            numberofdevices = ''
            upgradepriority = ''
            upgraderequired = ''
            row = [model,provdevices,regdevices,certified_fw,
                tested_fw,
                type,
                firmware,numberofdevices,
                customer_certified,cisco_tested,compatibilty,
                upgraderequired,upgradepriority]
            rows.append(row)
        
    # print(rows)
    analysis_df = DataFrame(rows,columns=['Model', 'Provisioned Devices', 'Registered Devices','Certified Firmware',
                                             'Cisco Tested Firmwares',
                                             'Type',
                                             'Firmware Versions','Registered Devices on the Firmware',
                                             'Customer Certified','Cisco Tested','Compatibility',
                                             'Upgrade Required','Upgrade Priority'])
    analysis_df.set_index(['Model', 'Provisioned Devices', 'Registered Devices','Certified Firmware'
                              ,'Cisco Tested Firmwares'
                              , 'Type'], inplace=True)
    # print(analysis_df.head())
    return analysis_df



#analysis = perform_analysis('C:\HSBC\\11.5 Upgarde\Automation\Version 4\\reg.xlsx')
# print(json.dumps(analysis, sort_keys=True, indent=4))
#write_analysis_to_excel_pandas(analysis)