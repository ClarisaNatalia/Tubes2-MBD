from Transaction import Transaction
from Resource import Resource


class Schedule:
    def __init__(self, ScheduleString):
        """
        Format of TransactionString: timestamp-operation-resource
        operation name written in all caps and not disingkat (singkat bahasa inggrisnya apa kwoakwo)
        Example:
        5-READ-X

        Multiple operations from different transactions are separated by commas
        Example :
        5-READ-X,2-READ-Y,1-READ-Y,3-WRITE-Z

        Contoh full schedule dari video kuliah MBD
        https://www.youtube.com/watch?v=AlrmbPO7Ovc&list=PLRdh21P3pZqvKMHZoWbyXOnIjnoT63NPK&index=1&t=342s

        5-READ-X,2-READ-Y,1-READ-Y,3-WRITE-Y,3-WRITE-Z,5-READ-Z,2-READ-Z,1-READ-X,4-READ-W,3-WRITE-W,5-WRITE-Y,5-WRITE-Z
        """
        # ATTRIBUTES
        self.resources = {}
        self.transactions = {}

        # IDENTIFY TRANSACTIONS AND RESOURCES
        regdTrans = [] # catat trans yg udah dibuat obj nya
        regdResourc = [] # catat resource yg udah dibuat obj nya

        splitToOperations = ScheduleString.split(',')
        for i in range(len(splitToOperations)): #i ADALAH URUTAN DIA DI SOAL
            splitToOperations[i] = splitToOperations[i].split('-')

            # create transaction obj and register operation if transaction obj hasnt been made, add doang if exists already
            timestamp = int(splitToOperations[i][0])
            if(timestamp not in regdTrans):
                # create obj
                tr = Transaction(timestamp)
                self.transactions[timestamp] = tr

                # insert operation
                self.transactions[timestamp].insertOperation(splitToOperations[i][1], splitToOperations[i][2], i) # kind, resource, order
                # self.transactions[timestamp].printYgsy()

                # add to registered
                regdTrans.append(timestamp)
            
            else:
                # add
                self.transactions[timestamp].insertOperation(splitToOperations[i][1], splitToOperations[i][2], i) # kind, resource, order

            # same thing, but resource objects
            resource_name = splitToOperations[i][2]
            if(resource_name not in regdResourc):
                # create obj
                resobj = Resource(resource_name)

                # add to resources list
                self.resources[resource_name] = resobj
                # self.resources[resource_name].printerNiBhovst()

                # add to registered
                regdResourc.append(resource_name)

        #for b, a in self.transactions.items():
        #    a.startread()
        #    a.finishread()
    
    def getResources(self):
        return self.resources

    def getTransaction(self):
        return self.transactions

    def getSpecifidTransaction(self, timestamp):
        for b, a in self.transactions.items():
            if a.getTimestamp() == timestamp:
                return a
            else:
                continue

    def printTransactions(self):
        for key, value in self.transactions.items():
            value.printYgsy()
    
    def getTopMostOp(self):
        ts_and_order = {}
        for timestamp, trans_obj in self.transactions.items():
            if(not(trans_obj.isZeroOperation())):
                ts_and_order[timestamp] = trans_obj.getTopMostOrderOnly()

        try:
            ts_to_get = min(ts_and_order, key=ts_and_order.get)
            return self.transactions[ts_to_get].getTopMostOperation()
        except:
            return None

#Schedule("5-READ-X,2-READ-Y,1-READ-Y,3-WRITE-Y,3-WRITE-Z,5-READ-Z,2-READ-Z,1-READ-X,4-READ-W,3-WRITE-W,5-WRITE-Y,5-WRITE-Z")
