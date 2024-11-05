



class SymbolTable:
    def __init__(self):
        self.globalTable = MiniTable(None)
        self.cur = self.globalTable
        self.id = 0
        self.params = []



    def enterScope(self,mini):
        #print("IN")
        self.cur.minis[mini] = MiniTable(self.cur)
        self.cur = self.cur.minis[mini]

    def enterNewScope(self):
        #print("IN")
        self.cur.minis[str(self.id) + "mini"] = MiniTable(self.cur)
        self.cur = self.cur.minis[str(self.id) + "mini"]
        self.id +=1

    def exitScope(self):
        #print("OUT")
        if self.cur.upper is not None:
            self.cur = self.cur.upper
    
    def lookUp(self,var):
        #print("LOOKUP " + var)
        self.addParams()
        temp_cur = self.cur
        while temp_cur is not None:
            #print(temp_cur.names)
            if var in temp_cur.names:
                return temp_cur.names[var]
            temp_cur = temp_cur.upper
        return -1;

    def fieldLookUp(self,base,name):    
        '''
        self.addParams()
        res = None
        temp_cur = self.cur
        while temp_cur is not None:
            #print(temp_cur.names)
            if base in temp_cur.names:
                res = temp_cur.names[base]
                break
            temp_cur = temp_cur.upper
        return -1'''

    def add(self,var):
        #print("ADD")
        self.cur.names[var['name']] = var['id']

    def setID(self,name,ID):
        #print(name)
        #print("Setting " + name + " to " + str(ID) +" in " + str(vars(self.cur)) )
        self.cur.names[name] = ID

    def setIDConst(self,name,ID):
        #print(name)
        #print("Setting " + name + " to " + str(ID) +" in " + str(vars(self.cur)) )
        if name in self.cur.names:
            self.cur.names[name] += [ID]
        else:
            self.cur.names[name] = [ID]

    def recordParam(self,param,id):
        self.params += [(param,id)]

    def addParams(self):
        for param in self.params:
            self.setID(param[0],param[1])
        self.params = []

    def returnAllVars(self):
        vars = []
        #print(self.cur.names)
        for name in self.cur.names.values():
            if name[0].__class__.__name__ == 'variable_record':
                vars += [name[0]]
        return vars
        
class MiniTable:
    def __init__(self,upper):
        self.names = {}
        self.upper = upper
        self.minis = {}