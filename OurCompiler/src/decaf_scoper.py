



class SymbolTable:
    def __init__(self):
        self.globalTable = MiniTable(None)
        self.cur = self.globalTable
        self.id = 0
        self.params = []
        self.lookUps = []



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
            temp = self.cur
            self.cur = self.cur.upper
            for key, value in self.cur.minis.items():
                if value == temp:
                    return key 
        return None
    
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

    def addFieldLookUp(self,base,name):
        self.lookUps += [(base,name,self.cur)]

    def executeFieldLookUps(self):
        for l in self.lookUps:
            self.cur = l[2]
            self.fieldLookUp(l[0],l[1])

    def fieldLookUp(self,base,name):   
        print(name) 
        print(base)
        if base.__class__.__name__ == 'referenceExpression_record':
            
            if base.ref_type == 'super':
                #handle super
                print("FIELD LOOKUP " + str(base) + ", " + str(name))
                self.addParams()
                res = None
                temp_cur = self.cur
                while temp_cur is not None:
                    if temp_cur.upper != None:
                        clazz = False
                        print(temp_cur.upper.minis)
                        for n in temp_cur.upper.names.values():
                            print(n)
                            if (n[0].__class__.__name__ == 'class_record'):
                                    clazz = True
                                    break
                        if clazz:
                            print(vars(temp_cur))
                            print(vars(temp_cur.upper))
                            supName = None
                            for k,v in temp_cur.upper.names.items():
                                if(temp_cur.upper.minis[v[0].miniName] == temp_cur):
                                    print(v[0])
                                    print(v[0].superName)
                                    supName = v[0].superName
                                    break
                            if(supName == None):
                                return -1
                            
                            supMini = None
                            for k,v in temp_cur.upper.names.items():
                                if(k == supName):
                                    print(v[0])
                                    supMini = v[0].miniName
                                    break
                            if(supMini == None):
                                return -1

                            for k,v in temp_cur.upper.minis[supMini].names.items():
                                if k == name :
                                    return v[1]
                            return -1
                            
                            return -1
                    temp_cur = temp_cur.upper
                return -1
                        



            else:

                #handle this
                print("FIELD LOOKUP " + str(base) + ", " + str(name))
                self.addParams()
                res = None
                temp_cur = self.cur
                while temp_cur is not None:
                    if temp_cur.upper != None:
                        clazz = False
                        print(temp_cur.upper.minis)
                        for n in temp_cur.upper.names.values():
                            print(n)
                            if (n[0].__class__.__name__ == 'class_record'):
                                clazz = True
                        if clazz == True:
                            print("we found it " + str(vars(temp_cur)))
                            for k,v in temp_cur.names.items():
                                if k == name :
                                    return v[1]
                            return -1
                    temp_cur = temp_cur.upper
                return -1

          
                




        #This part is normal look up
        base = base.name
        print("FIELD LOOKUP " + str(base) + ", " + str(name))
        self.addParams()
        res = None
        temp_cur = self.cur
        while temp_cur is not None:
            print(temp_cur.names)
            print(temp_cur.names.keys())
            if base in temp_cur.names.keys():
                print(temp_cur.names[base][0])
                if temp_cur.names[base][0].__class__.__name__ == 'variable_record':
                    base = temp_cur.names[base][0].type
                    print("New base " + base)
                else:
                    res = temp_cur.names[base][0]
                    print("Found the base " + str(res))
                    break
            temp_cur = temp_cur.upper
        if res !=None:
            print(str(temp_cur.minis))
            for k,v in temp_cur.minis.items():
                if k == name:
                    return v[1]
        print("FIELD LOOKUP")
        return -1

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