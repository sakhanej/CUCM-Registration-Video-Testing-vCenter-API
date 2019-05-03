## How to Use the Script:
**Step 1**: Prepare the input file:
-	Input file should be an excel workbook (in .xlsx) format comprising of two worksheets named **Test Endpoints** and **Production Endpoints**
-	Fill in the Test Endpoints worksheet with all the test endpoints and bridge (Codian / CMS / Movi) details. Note, if the IP-address is left empty the script will consider the test endpoint as a bridge .Following details will be required:
    - Name of the Endpoint – Column heading should be ‘Name’
    - IP Address of the Endpoint – Column heading should be ‘IP Address’
    - Admin Username for the Endpoint – Column heading should be ‘Username’
    - Admin Password for the Endpoint – Column heading should be ‘Password’
    - Auto answer enabled / disabled for the Endpoint – Column heading should be ‘Auto Answer’
-	Fill in the Production Endpoints worksheet with all the production endpoints details. Following details will be required:
    - Name of the Endpoint – Column heading should be ‘Name’
    - IP Address of the Endpoint – Column heading should be ‘IP Address’
    - Admin Username for the Endpoint – Column heading should be ‘Username’
    - Admin Password for the Endpoint – Column heading should be ‘Password’
    - Auto answer enabled / disabled for the Endpoint – Column heading should be ‘Auto Answer’

**Step 2**: Execute the Script either using the terminal (python <script path along with script name followed by .py extension>) or the exe file:
-	Enter the path for the Input File.
- Enter the name of the Input File.
- Script also Supports to do a lookup from the corporate directory (TMS / UDS phonebook) so input the String that can be searched from the corporate directory.
- Since signaling takes time, the script is designed to provide a timeout before receiving calls from the far end, by default it is 4 seconds you can tweak this when prompted.
- Post this the script will start executing and you will see what’s going on in the back end
- Once the execution is finished the results will be written in an excel and the excel will be stored in the same path as that of the input file and the name of the file would be **<Input Filename>_output_DDMMYYYY_HHMMSS.xlsx**

**Sample Scenario:**
- **Test endpoints**: Cincinnati Phone 1 , CMS Bridge
- **Production endpoints**: Singapore Phone 3
- **Timeout value**: 4
- **Output**:
```
Testing for Singapore Phone 3
Placing call from Singapore Phone 3 to Cincinnati Phone 1
Timing out for 4 second
Reading call-id from Cincinnati Phone 1
Receiving call from Cincinnati Phone 1
Reading call statistics from Singapore Phone 3
Disconnecting call from Cincinnati Phone 1
Placing call from Cincinnati Phone 1 to Singapore Phone 3
Timing out for 4 second
Reading call-id from Singapore Phone 3
Receiving call from Singapore Phone 3
Reading call statistics from Cincinnati Phone 1
Disconnecting call from Singapore Phone 3
Placing call from Singapore Phone 3 to CMS Bridge
Timing out for 4 second
Reading call-id from Singapore Phone 3
Reading call statistics from Singapore Phone 3
Disconnecting call from Singapore Phone 3
```

**Step 3**: Check the output of the script and results:.

## Runtime Exceptions
This section talks about different kinds of runtime exceptions you can get while executing the script.
- The script uses requests package to communicate with the endpoints so you can expect all the exceptions that are part of this package to have a look at the visit this [link](http://docs.python-requests.org/en/master/_modules/requests/exceptions/).
- The script also has a custom Exception class that is inherited from the python inbuilt exception class which handles the following exceptions primarily:
  - Incorrect credentials for a device
  - Unable to Dial out from a device
  - Unable to read the call-id from a device
  - Unable to receive calls from a device
  - Unable to read call statistics from a device
  - Unable to disconnect call from the device
