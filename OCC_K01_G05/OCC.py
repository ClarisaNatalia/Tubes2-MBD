from Resource import Resource
from Schedule import Schedule
import copy

from Transaction import Transaction

class OCC:
    #Fungsi pengecekan apakah terdapat irisan antara dua array 
    def isintersec(self,a,b):
        intersec = False
        if(len(list(set(a) & set(b))) != 0):
            intersec = True
        
        return intersec

    def __init__(self, ScheduleString):
        self.sched = Schedule(ScheduleString)
        self.resourceVersions = {}
        for name, resource_obj in self.sched.getResources().items():
            # key is RESOURCE NAME, value is DICT OF RESOURCE  VERSIONS
            # initalize with ver 0
            self.resourceVersions[name] = {0 : resource_obj}
        
        print("Detected transactions :")
        self.sched.printTransactions()

        print("All resources initialized :")
        for res, versions in self.resourceVersions.items():
            for vernum, resource in versions.items():
                resource.printerNiBhovst()

        trans = self.sched.getTransaction()

        #setting parameter di transaksi
        for i in (trans):
            trans[i].startread()
            trans[i].finishread()
            trans[i].lastWrite()
            trans[i].setReadsource()
            trans[i].setWritesource()
        
        op = self.sched.getTopMostOp()
        count = 0
        print("")

        #memulai OCC
        print("Start OCC")
        print("")
        while(op != None):
            validate = False
            if(op.getKind() == 'READ'):
                op.doOperation()

            else: # op.getKind() == 'WRITE'
                #validate = False
                #CHECKING VALID ATO ENGGAK 
                #1. Finish(Tj)<Starts(Ti) HARUS SEMUA TRANSAKSI
                for b, i in trans.items():
                    if(i.getTimestamp() != op.getTimestamp()):
                        if((trans[op.getTimestamp()].getstartread())<i.getLastwrite()):
                            validate = True
                            break

                #2. startTS(Tj) < finishTS(Ti) < validationTS(Tj) and the set of data items written by Ti does not intersect with the set of data items read by Tj. 
                if(validate == False): 
                    for b, i in trans.items():
                        if(i.getTimestamp() != op.getTimestamp()):
                            if(i.getstartread()< trans[op.getTimestamp()].getLastwrite()< i.getfinishread() and self.isintersec(trans[op.getTimestamp()].getReadresource(),i.getWriteresource()) == False):
                                validate = True
                                break

                if(validate == True):
                    if(trans[op.getTimestamp()].getfinishread()-1 == count):
                        print("T"+str(op.getTimestamp()), "validated")  
                    op.doOperation()
                else:
                    #penanganan fail
                    op.failOperation()
                    trans[op.getTimestamp()].insertOperation(op.getKind(),op.getResource(),count) #memasukkan kembali operasi yang fail ke dalam transaksi dengan urutan baru, yaitu count
                    trans[op.getTimestamp()].lastWrite() #update lastwrite yang dilakukan oleh transaksi 
            
            if(trans[op.getTimestamp()].isZeroOperation()):
                print("T"+str(op.getTimestamp()), "is successfull")    

            op = self.sched.getTopMostOp()
            count += 1
    

OCC("5-READ-X,2-READ-Y,1-READ-Y,5-READ-Z,2-READ-Z,1-READ-X,4-READ-W,5-WRITE-Y,5-WRITE-Z")
#OCC("1-READ-B,2-READ-B,2-READ-A,1-READ-A,2-WRITE-B,2-WRITE-A")