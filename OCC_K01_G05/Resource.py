class Resource:
    def __init__(self, name):
        self.name = name

    # GETTER
    def getName(self):
        return self.name

    # PRINT ya ges ya
    def printerNiBhovst(self):
        print("Resource :"+self.name)
        #print("RTS :"+str(self.r_timestamp))
        #print("WTS :"+str(self.w_timestamp))
        #print("")