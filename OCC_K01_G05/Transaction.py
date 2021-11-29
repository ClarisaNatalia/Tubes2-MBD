#from _typeshed import Self
from Resource import Resource

class Operation:
    def __init__(self,timestamp, kind, resource, order):
        self.timestamp = timestamp
        self.kind = kind
        self.resource = resource
        self.order = order
    
    # GETTER
    def getKind(self):
        return self.kind

    def getTimestamp(self):
        return self.timestamp

    def settimestamp(self,a):
        self.timestamp = a

    def getResource(self):
        return self.resource
    
    def getOrder(self):
        return self.order
    
    def printOp(self):
        print("["+str(self.order)+"] T"+str(self.timestamp)+" "+self.kind+" "+self.resource)

    def doOperation(self):
        print("["+str(self.order)+"] T"+str(self.timestamp)+" "+self.kind+" "+self.resource+" is done successfully")
    
    def failOperation(self):
        print("["+str(self.order)+"] T"+str(self.timestamp)+" "+self.kind+" "+self.resource+" failed. Rolling back...")
        print("")

class Transaction:
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.mulairead = 0
        self.selesairead = 0
        self.lastwrite = 0
        self.operations = []
        self.readresource = []
        self.writeresource = []

    def insertOperation(self, kind, resource, order):
        op = Operation(self.timestamp, kind, resource, order)
        self.operations.append(op)

    def getTopMostOrderOnly(self):
        if (len(self.operations) > 0):
            return self.operations[0].getOrder()
        else:
            return None

    def getTopMostOperation(self):
        topmost = self.operations.pop(0)
        # print("This is after popping")
        # self.printYgsy()
        return topmost

    def printYgsy(self):
        print("T"+str(self.timestamp))
        for i in self.operations:
            i.printOp()
        print("")

    def isZeroOperation(self):
        if (len(self.operations) == 0):
            return True
        return False

    def startread(self):#dengan asumsi bahwa semua transaksi pasti dimulai dengan read
        self.mulairead = self.operations[0].getOrder()
        #print('startread', self.operations[0].getOrder())

    def getstartread(self):
        return self.mulairead

    def finishread(self):
        for i in range(len(self.operations)):
            if(self.operations[i].getKind() == 'READ'):
                continue
            elif(self.operations[i].getKind() == 'WRITE'): #ketemu write pertama kali
                self.selesairead = self.operations[i].getOrder()
                
        if(self.operations[len(self.operations)-1].getKind() == 'READ'):    
            self.selesairead = 100

        #print('finishread', self.operations[i].getOrder())

    def getfinishread(self):
        return self.selesairead

    def getTimestamp(self):
        return self.timestamp

    def lastWrite(self):
        if(self.operations[-1].getKind() == 'WRITE'):
            self.lastwrite = self.operations[-1].getOrder()
        
    def getLastwrite(self):
        return self.lastwrite

    def setReadsource(self):
        for val in self.operations:
            if(val.getKind() == 'READ'):
                (self.readresource).append(val.getResource())
                #print(val.getResource())
    
    def getReadresource(self):
        return self.readresource
    
    def setWritesource(self):
        for val in self.operations:
            if(val.getKind() == 'WRITE'):
                (self.readresource).append(val.getResource())
                #print(val.getResource())

    def getWriteresource(self):
        return self.writeresource

    def getoperation(self):
        return self.operations