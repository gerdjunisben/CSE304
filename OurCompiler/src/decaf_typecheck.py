# Benjamin Gerdjunis 
# SB ID: 115962358
# Net ID: bgerdjunis
# Donato Zampini
# SB ID: 114849209
# Net ID: dzampini

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
    
    def addValidForLoop(self,initialize,conditional,update,thing):
        self.checkQueue += [(3,initialize,conditional,update,thing)]

    def addValidReturn(self,returnVal,thing):
        self.checkQueue += [(4,returnVal,thing)]


    def addMethodReturn(self,methodReturn):
        for i in range(0,len(self.checkQueue)):
            if self.checkQueue[i][0] == 4 and len(self.checkQueue[i])==3:
                self.checkQueue[i] = self.checkQueue[i][:3] + (methodReturn,) 


    def executeQueue(self):
        for thing in self.checkQueue:
            if(thing[0] ==0):
                res = self.validTypes(thing[1].type,thing[2].type)
                if(res):
                    thing[3].type = thing[2].type
                else:
                    thing[3].type = 'error'
                    raise SyntaxError(f"Type mismatch between {thing[1].type} on line {thing[1].line} and {thing[2].type} on line {thing[2].line}")
            elif (thing[0] == 1):
                res = self.checkValid(thing[1],thing[2])
                if(res==None):
                    thing[3].type = 'error'
                    raise SyntaxError(f"Type mismatch between {thing[1].type} on line {thing[1].line} invalid type for surrounding context")
                else:
                    thing[3].type = res
            elif (thing[0] == 3):
                res1 = self.validTypes(thing[1].type,thing[3].type)
                res2 = self.checkValid(thing[2],{'bool'})
                if(res2 == None or res1 == None):
                    thing[4].type = 'error'
                    raise SyntaxError(f"Invalid for loop either {thing[1].type} on line {thing[1].line} and {thing[3].type} on line {thing[3].line} mismatch or {thing[2].type} on line {thing[2].line} is not a bool")
                else:
                    thing[4].type = res2
            elif(thing[0] == 4):
                res = self.validTypes(thing[1],thing[3])
                if(res==None):
                    thing[2].type = 'error'
                    raise SyntaxError(f"Type mismatch between returned value and header return {thing[1].type} on line {thing[1].line} and {thing[3].type} on line {thing[3].line}")
                else:
                    thing[2].type = thing[1]

            else:
                res = self.validBinary(thing[1],thing[2],thing[3])
                if(res==None):
                    thing[4].type = 'error'
                    raise SyntaxError(f"Invalid binary op involving {thing[1].type} on line {thing[1].line} and {thing[2].type} on line {thing[2].line} involving operation {thing[3]}")
                else:
                    thing[4].type = res
        self.checkQueue = []


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
            leftRes = self.checkValid(left,{'bool'})
            rightRes = self.checkValid(right,{'bool'})
            if(leftRes != None and rightRes != None):
                return 'bool'
            else:
                return None
        elif(op == "comparison"):
            leftRes = self.checkValid(left,{'float','int'})
            rightRes = self.checkValid(right,{'float','int'})
            if(leftRes != None and rightRes != None):
                return 'bool'
            else:
                return None
        else:
            if(self.validTypes(left.type,right.type) or self.validTypes(right.type,left.type)):
                return 'bool'
            else:
                return None
    
    def validTypes(self,main,sub):
        if(sub== 'error' or main == 'error'):
            return False
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
typeChecker.addType('bool','void')
typeChecker.addType('object','void')
