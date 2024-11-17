# Benjamin Gerdjunis 
# SB ID: 115962358
# Net ID: bgerdjunis
# Donato Zampini
# SB ID: 114849209
# Net ID: dzampini

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

    def addArgs(self,thing,args,method):
        for i in range(0,len(self.lookUps)):
            if self.lookUps[i][3] == thing:
                self.lookUps[i] = self.lookUps[i][:3] + (method,) + (args,)
                break

    def addFieldLookUp(self,base,name,thing):
        self.lookUps += [(base,name,self.cur,thing)]

    def executeFieldLookUps(self):
        for l in self.lookUps:
            self.cur = l[2]
            if(len(l)<5):
                l+=([],)
            temp = self.fieldLookUp(l[0],l[1],l[4])
            l[3].id = temp[1]
            if temp[0].__class__.__name__ == 'method_record':
                l[3].type = temp[0].returnType
            elif temp[0].__class__.__name__ == 'field_record':
                l[3].type = temp[0].type
            else:
                l[3].type = l[1]
        self.lookUps = []

    def fieldLookUp(self, base, name, args):
        self.addParams()
        def validate_parameters(expected_params, given_args):
            if len(expected_params) != len(given_args):
                return False
            for param, arg in zip(expected_params, given_args):
                if not typeChecker.validTypes(param.type, arg.type):
                    return False
            return True

        def find_in_table(table, name, args):
            if not table or name not in table.names:
                return None
            entries = table.names[name]
            if isinstance(entries, list):  # Constructor list
                for entry in entries:
                    if entry[0].__class__.__name__ == 'constructor_record' and validate_parameters(entry[0].parameters, args):
                        return entry
            elif entries[0].visibility and (not hasattr(entries, 'parameters') or validate_parameters(entries[0].parameters, args)):
                return entries
            return None

        if base.__class__.__name__ == 'referenceExpression_record':  # self/super
            base = base.className
            return find_in_table(typeChecker.types.get(base).miniTable, name, args)

        if isinstance(base, str) and base in typeChecker.types:  # new keyword
            return find_in_table(typeChecker.types[base].miniTable, name, args)

        if hasattr(base, 'name') and base.name in typeChecker.types:  # Class literal
            return find_in_table(typeChecker.types[base.name].miniTable, name, args)

        if hasattr(base, 'type'):  # Instance
            base = base.type
            return find_in_table(typeChecker.types.get(base).miniTable, name, args)

        return None



        

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