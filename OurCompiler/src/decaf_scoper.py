
from decaf_typecheck import typeChecker

class SymbolTable:
    def __init__(self):
        self.globalTable = MiniTable(None)
        self.cur = self.globalTable
        self.id = 0
        self.params = []
        self.lookUps = []
        self.refs = []

    def addRef(self,reference):
        self.refs += [reference]

    def setRefs(self,className):
        for r in self.refs:
            if r.ref_type == 'this':
                r.className = className
            else:
                r.className = typeChecker.types[className].parent
        self.refs = []

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
                    return value 
        return None
    
    def lookUp(self,var):
        #print("LOOKUP " + var)
        self.addParams()
        if(var in typeChecker.types):
            return (var,var)
        temp_cur = self.cur
        while temp_cur is not None:
            #print(temp_cur.names)
            #print(temp_cur.names)
            if var in temp_cur.names:
                return temp_cur.names[var]
            temp_cur = temp_cur.upper
        return -1;

    def addArgs(self,thing,args):
        for i in range(0,len(self.lookUps)):
            if self.lookUps[i][3] == thing:
                self.lookUps[i]+= (args,)
                break

    def addFieldLookUp(self,base,name,thing):
        self.lookUps += [(base,name,self.cur,thing)]

    def executeFieldLookUps(self):
        for l in self.lookUps:
            self.cur = l[2]
            if(len(l)<5):
                l+=([],)
            self.fieldLookUp(l[0],l[1],l[4])

    def fieldLookUp(self,base,name,args):   
        #print(name) 
        #print(base)
        self.addParams()
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>handle self and super
        if base.__class__.__name__ == 'referenceExpression_record':
            base = base.className
            if(typeChecker.types[base].miniTable == None):
                return -1
            for k,v in typeChecker.types[base].miniTable.names.items():
                #print(k + " " + str(v))
                if k == name and v[0].visibility != None:
                    if (v[0].__class__.__name__ =='method_record' or v[0].__class__.__name__ =='constructor_record') and v[0].applicability == None :
                        valid = True
                        for i in range(0,len(v[0].parameters)):
                            if not typeChecker.validTypes(v[0].parameters[i].type,args[i].type):
                                valid=False
                                break
                        if(valid):
                            print("Found self/super:" + name + " in " + base)
                            return v[1]
                        return -1
                    print("Found self/super:" + name + " in " + base)
                    return v[1]
            return -1;
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>handle new
        elif(isinstance(base,str) and base in typeChecker.types):
            if(typeChecker.types[base].miniTable == None):
                return -1
            for k,v in typeChecker.types[base].miniTable.names.items():
                #print(k + " " + str(v))
                if k == name and isinstance(v,list): #go through the constructor list
                    for c in v:
                        if  (c[0].__class__.__name__ =='method_record' or c[0].__class__.__name__ =='constructor_record') :
                            valid = True
                            for i in range(0,len(c[0].parameters)):
                                if not typeChecker.validTypes(c[0].parameters[i].type,args[i].type):
                                    valid=False
                                    break
                            if(valid):
                                print("Found constructor:" + name + " in " + base)
                                return c[1]
                            return -1
            return -1;
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>handle class literal
        elif(base.name in typeChecker.types):
            base = base.name
            if(typeChecker.types[base].miniTable == None):
                return -1
            for k,v in typeChecker.types[base].miniTable.names.items():
                #print(k + " " + str(v))
                if k == name and v[0].visibility != None:
                    if (v[0].__class__.__name__ =='method_record' or v[0].__class__.__name__ =='constructor_record') and v[0].applicability != None:
                        valid = True
                        for i in range(0,len(v[0].parameters)):
                            if not typeChecker.validTypes(v[0].parameters[i].type,args[i].type):
                                valid=False
                                break
                        if(valid):
                            print("Found literal:" + name + " in " + base)
                            return v[1]
                        return -1
                    print("Found literal:" + name + " in " + base)
                    return v[1]
            return -1;
        else: #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>handle instance
            base = base.type.type
            if(typeChecker.types[base].miniTable == None):
                return -1
            for k,v in typeChecker.types[base].miniTable.names.items():
                #print(k + " " + str(v))
                if k == name and v[0].visibility != None :
                    if (v[0].__class__.__name__ =='method_record' or v[0].__class__.__name__ =='constructor_record') and v[0].applicability == None :
                        if(len(args) == len(v[0].parameters)):
                            valid = True
                            for i in range(0,len(v[0].parameters)):
                                if not typeChecker.validTypes(v[0].parameters[i].type,args[i].type):
                                    valid=False
                                    break
                            if(valid):
                                print("Found instance:" + name + " in " + base)
                                return v[1]
                            return -1
                    print("Found instance:" + name + " in " + base)
                    return v[1]
            return -1;




        

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

    def removeParam(self,name):
        #print(str(self.params))
        #print(name)
        for i in range(0, len(self.params)):
            if self.params[i][0] == name:
                del self.params[i]
                break
        #print(str(self.params))

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