class Service(Object):
'''
This is an abstract Class which creates a Service as an object. Contains following attributes:

Attributes :
            name : Name of Service
            status : State of service [ running etc.]
            Start_time : time at which service is started
            up_time : How long service is in up state
'''

## Contructor
    def __init__(self,name):
        self.name=name
        self.setattr(status=None, start_time=None, up_time=None)

    def setattr(self,**kwargs):
        for attribute,value in kwargs.items():
            self.__dict__[attribute]=value
    
    def getattr(self,**kwargs):
        print (kwargs.items())

    def get_name(self):
        return self.name

    def get_status(self):
        if self.status==None
            return "Not_Initialised"
        else:
            return self.status

    def get_start_time(self):
        if self.start_time==None
            return "Not_Initialised"
        else:
            return self.start_time

    def get_up_time(self):
        if self.up_time==None
            return "Not_Initialised"
        else:
            return self.up_time


    
    def get_details(self):
        returndict={Name:self.name, Status:self.status, Start_time:self.start_time, Up_time:self.up_time}



print ("hello")
First=Service("Tomcat")
print (First.name)