class typeTree:
    def __init__(self):
        self.root = typeNode('void',None)
        self.types = {'void':self.root}

    def addType(self,name,sup):
        if (self.types[sup] == None):
            return None
        self.types[sup].children[name] = typeNode(name,sup)
        self.types[name] = self.types[sup].children[name]
        

    def addUsertype(self,name,sup,miniTable):
        if (self.types[sup] == None):
            return None
        self.types[sup].children[name] = typeNode(name,sup,miniTable)
        self.types[name] = self.types[sup].children[name]

    def superOfName(self,name):
        if (self.types[name] == None):
            return None
        return self.types[name].parent
    
    def validTypes(self,main,sub):
        
        while(self.types[sub].parent!=None):
            if(main == sub or sub =='null'):
                return True
            sub = self.types[sub].parent

        return False



class typeNode:
     def __init__(self,name,parent,miniTable=None):
        self.name = name
        self.parent = parent
        self.children = {'null':None}
        self.miniTable = miniTable


typeChecker = typeTree()
typeChecker.addType('float','void')
typeChecker.addType('int','float')
typeChecker.addType('boolean','void')
typeChecker.addType('object','void')