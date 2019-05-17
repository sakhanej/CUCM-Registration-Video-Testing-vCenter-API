## Overview
This repository can provide you python scripts which can be used:

#### Unified Collaboration Products
  1. CUCM Registration Reports
  2. UC Services Status
  3. CUCM Firmware Analysis
  4. CUCM Login Checks (verifies if LDAP users can login)
#### Video Endpoints
  5. Migrating Endpoints from VCS to CUCM
  6. Operational Readiness Testing(ORT) of Video Endpoints
#### vCenter
  7. Vcenter Specifications

## Pre-Requisites
Following are the pre-requisites for the script to function properly:

 - Refer **requirements.txt** for python version and libraries required to run the scripts.
 - Convert python scripts to executable files (here is a small [video](https://www.youtube.com/watch?v=lOIJIk_maO4) on how it can be done).
 - **Unified Collaboration Products**:
    - Make sure following services are functioning properly:
        - SOAP ( Real-Time Service APIs and Performance Monitoring APIs)
        - Cisco AXL Web Service
    - Configure 1 application user with following roles:
        - Standard AXL API Access
        - Standard CCM Admin Users
        - Standard CUReporting
        - Standard RealtimeAndTraceCollection
        - Standard SERVICEABILITY Administration
    - Make sure you can access CUCM WSDL (as this script uses WSDL Implementation). Links to check:
        - **Verify AXL**: https://ipaddress:8443/axl/
        - **Verify ServiceWSDL**: https://ipaddress:8443/controlcenterservice/services/ControlCenterServicesPort
        - **Verify RISWSDL**: https://ipaddress:8443/realtimeservice2/services/RISService70?wsdl
    - For Login Checks, web scrapping mechanism is used.
  
  - **Video Endpoints**:
    - Endpoints should have web-access enabled since the script uses XML-Based API’s for Endpoints, preferably HTTP + HTTPS.
    - Endpoint should be running on TC7.3.6 or above / CE8.X / CE9.X, lower firmware versions have not been tested.
    - The system executing the script should be able to access the webpage of the endpoints ensuring the IP reachability.
    - There should be a dedicated set of test endpoints and bridges reserved for testing that can be used by this script.
 - **vCenter**
    - The scripts uses vCenter API implemented using Managed Object Browser(MOB) of vCenter.
    - By default, MOB is disabled on ESX/ESXi 6.x servers, and will need to be manually enabled.  To test if MOB  is enabled,       follow the steps below:
      1. Enter following URL in a browser, where x.x.x.x is the IP Address of the vCenter Server or ESX host:
          http://x.x.x.x/mob
      2. If MOB is enabled, the server will likely prompt you for credentials, and once entered, it will display the MOB                Properties and Methods
      3. If MOB is not enabled, the server will likely return an "HTTP 503 - Service Unavailable" error
    - To Enable MOB on an ESX Server and vCenter Server:
        - Visit "https://community.ipswitch.com/s/article/How-to-Enable-vmware-Managed-Object-Browser-MOB-on-an-ESX-Host-or-                    vCenter-Server"
