class typeTree:
    def __init__(self):
        self.root = typeNode('void',None)
        self.types = {'void':self.root}
        self.checkQueue = []

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
    
    def addValidTypes(self,main,sub,thing):
        self.checkQueue += [(0,main,sub,thing)]

    def addCheckValid(self,main,types,thing):
        self.checkQueue += [(1,main,types,thing)]

    def addValidBinary(self,left,right,op,thing):
        self.checkQueue += [(2,left,right,op,thing)]

    def executeQueue(self):
        for thing in self.checkQueue:
            if(thing[0] ==0):
                res = self.validTypes(thing[1].type,thing[2].type)
                if(res):
                    thing[3].type = thing[2].type
                else:
                    thing[3].type = 'error'
            elif (thing[0] == 1):
                res = self.checkValid(thing[1],thing[2])
                if(res==None):
                    thing[3].type = 'error'
                else:
                    thing[3].type = res
            else:
                res = self.validBinary(thing[1],thing[2],thing[3])
                if(res==None):
                    thing[4].type = 'error'
                else:
                    thing[4].type = res


    def validBinary(self,left,right,op):
        if(op == "arithmetic"):
            leftRes = self.checkValid(left,{'float','int'})
            rightRes = self.checkValid(right,{'float','int'})
            if(leftRes != None and rightRes != None):
                if(leftRes == 'float' or rightRes == 'float'):
                    return 'float'
                else:
                    return 'int'
            else:
                return None
        elif(op == "boolean"):
            leftRes = self.checkValid(left,{'boolean'})
            rightRes = self.checkValid(right,{'boolean'})
            if(leftRes != None and rightRes != None):
                return 'boolean'
            else:
                return None
        elif(op == "comparison"):
            leftRes = self.checkValid(left,{'float','int'})
            rightRes = self.checkValid(right,{'float','int'})
            if(leftRes != None and rightRes != None):
                return 'boolean'
            else:
                return None
        else:
            if(self.validTypes(left,right) or self.validTypes(right,left)):
                return 'boolean'
            else:
                return None
    
    def validTypes(self,main,sub):
        while(self.types[sub].parent!=None):
            if(main == sub or sub =='null'):
                return True
            sub = self.types[sub].parent
        return False
    
    def checkValid(self,thing,types):
        if(thing.type in types):
            return thing.type
        return None



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