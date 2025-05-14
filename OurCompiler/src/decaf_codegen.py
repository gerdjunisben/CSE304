# Benjamin Gerdjunis 
# SB ID: 115962358
# Net ID: bgerdjunis
# Donato Zampini
# SB ID: 114849209
# Net ID: dzampini


import decaf_parser as parser
import sys
from decaf_absmc import *
from decaf_typecheck import typeChecker

StorageMachine = TheStorageMachine(100)
staticFields = []

curIDs = {'return':StorageMachine.getArgs(1)[0],'one':StorageMachine.getNextTemp(),'zero':StorageMachine.getNextTemp()}

class ReturnRegister:
    def __init__(self):
        self.id = 'return'



returnRegister = ReturnRegister()


    
def mov_imm_cell(cell,cons):
    if(cons.type == 'int'):
        return mov_immed_i(cell.registerName,cons.value)
    elif(cons.type == 'float'):
        return mov_immed_f(cell.registerName,cons.value)
    else:
        if(cons.value == 'true'):
            return mov_immed_i(cell.registerName,1)
        else:
            return mov_immed_i(cell.registerName,0)
    

def processMethod(method):
    b =[]
    ret = None
    if(len(method.args) == 0):
        args = StorageMachine.getArgs(1)
    else:
        args = StorageMachine.getArgs(len(method.args)+1)
    for i in range(0,len(method.args) + 1):
        b+= [save(args[i].registerName)]
    if(method.base.__class__.__name__ != 'referenceExpression_record'):
        b+= handleSetting(args[0],method.base)
    for i in range(0,len(method.args)):
        b+= handleSetting(args[i +1],method.args[i])
    b+= [ call('M_' + method.method_name + '_' + str(method.id))]
    for i in range(1,len(method.args) +1):
        b+= [restore(args[i].registerName)]
    ret = (b,args[0])

    return ret

def processConstructor(memory,newStatement):
    b =[]
    ret = None
    if(len(newStatement.args) == 0):
        args = StorageMachine.getArgs(1)
    else:
        args = StorageMachine.getArgs(len(newStatement.args) + 1)
    for i in range(0,len(newStatement.args) + 1):
        b+= [save(args[i].registerName)]
    b+=[mov(args[0].registerName,memory.registerName)]
    for i in range(0,len(newStatement.args)):
        b+= handleSetting(args[i+1],newStatement.args[i])
    b+= [ call('C_'+str(newStatement.id))]
    for i in range(0,len(newStatement.args) +1):
        b+= [restore(args[i].registerName)]
    ret = b

    return ret

def processUnary(unary):
    ret = None
    b=[]
    if(unary.operation == '!'):
        temp = StorageMachine.getNextTemp()
        res = StorageMachine.getNextTemp()
        b+= handleSetting(temp,unary.operand)
        b+=[mov_immed_i(res.registerName,1)]
        b+=[isub(res.registerName,res.registerName,temp.registerName)]
        StorageMachine.freeRegister(temp)
        ret = (b,res)
    elif(unary.operation == '-'):
        temp = StorageMachine.getNextTemp()
        res = StorageMachine.getNextTemp()
        b+= handleSetting(temp,unary.operand)
        b+=[mov_immed_i(res.registerName,0)]
        b+=[isub(res.registerName,res.registerName,temp.registerName)]
        StorageMachine.freeRegister(temp)
        ret = (b,res)
    else:
        res = StorageMachine.getNextTemp()
        b+=[mov_immed_i(res.registerName,unary.operand.value)]
        ret = (b,res)
    return ret


def processBinary(binary):
    b = []
    ours = []
    ret = None
    if(binary.leftOperand.__class__.__name__ == 'const_record'):
        left = StorageMachine.getNextTemp()
        ours +=[left]
        b+=[mov_imm_cell(left,binary.leftOperand)]
    elif(binary.leftOperand.__class__.__name__ == 'varExpression_record'):
        left = curIDs[binary.leftOperand.id]
    elif(binary.leftOperand.__class__.__name__ == 'binaryExpression_record'):
        res = processBinary(binary.leftOperand)
        left = res[1]
        ours +=[left]
        b+= res[0]
    elif(binary.leftOperand.__class__.__name__ == 'unaryExpression_record'):
        res = processUnary(binary.leftOperand)
        left = res[1]
        ours +=[left]
        b+= res[0]
    elif(binary.leftOperand.__class__.__name__ == 'fieldAccessExpression_record'):
        left = StorageMachine.getNextTemp()
        ours += [left]
        out = resolveField(binary.leftOperand)
        b+= out[1]
        b+=[mov(left.registerName,out[0])]
    else:
        res = processMethod(binary.leftOperand)
        left = res[1]
        b+= res[0]


    if(binary.rightOperand.__class__.__name__ == 'const_record'):
        right = StorageMachine.getNextTemp()
        ours +=[right]
        b+=[mov_imm_cell(right,binary.rightOperand)]
    elif(binary.rightOperand.__class__.__name__ == 'varExpression_record'):
        right = curIDs[binary.rightOperand.id]
    elif(binary.rightOperand.__class__.__name__ == 'binaryExpression_record'):
        res = processBinary(binary.rightOperand)
        right = res[1]
        ours +=[right]
        b+= res[0]
    elif(binary.rightOperand.__class__.__name__ == 'unaryExpression_record'):
        res = processUnary(binary.rightOperand)
        right = res[1]
        ours +=[right]
        b+= res[0]
    elif(binary.rightOperand.__class__.__name__ == 'fieldAccessExpression_record'):
        right = StorageMachine.getNextTemp()
        ours += [right]
        out = resolveField(binary.rightOperand)
        b+= out[1]
        b+=[mov(right.registerName,out[0])]
    else:
        res = processMethod(binary.rightOperand)
        right = res[1]
        b+= res[0]





    if(binary.operation == '+'):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[iadd(res.registerName,left.registerName,right.registerName)]
        else:
            temp1 = StorageMachine.getNextTemp()
            temp2 = StorageMachine.getNextTemp()
            if(binary.leftOperand.type == 'int'):
                b+=[itof(temp1.registerName,left.registerName)]
            elif(binary.rightOperand.type == 'int'):
                b+=[itof(temp2.registerName,right.registerName)]
            b+=[fadd(res.registerName,temp1.registerName  if (binary.leftOperand.type == 'int') else left.registerName,temp2.registerName  if (binary.rightOperand.type == 'int') else right.registerName)]
            StorageMachine.freeRegister(temp1)
            StorageMachine.freeRegister(temp2)
        ret = (b,res)
    elif(binary.operation == '-'):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[isub(res.registerName,left.registerName,right.registerName)]
        else:
            temp1 = StorageMachine.getNextTemp()
            temp2 = StorageMachine.getNextTemp()
            if(binary.leftOperand.type == 'int'):
                b+=[itof(temp1.registerName,left.registerName)]
            elif(binary.rightOperand.type == 'int'):
                b+=[itof(temp2.registerName,right.registerName)]
            b+=[fsub(res.registerName,temp1.registerName  if (binary.leftOperand.type == 'int') else left.registerName,temp2.registerName  if (binary.rightOperand.type == 'int') else right.registerName)]
            StorageMachine.freeRegister(temp1)
            StorageMachine.freeRegister(temp2)
        ret = (b,res)
    elif(binary.operation == '*'):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[imul(res.registerName,left.registerName,right.registerName)]
        else:
            temp1 = StorageMachine.getNextTemp()
            temp2 = StorageMachine.getNextTemp()
            if(binary.leftOperand.type == 'int'):
                b+=[itof(temp1.registerName,left.registerName)]
            elif(binary.rightOperand.type == 'int'):
                b+=[itof(temp2.registerName,right.registerName)]
            b+=[fmul(res.registerName,temp1.registerName  if (binary.leftOperand.type == 'int') else left.registerName,temp2.registerName  if (binary.rightOperand.type == 'int') else right.registerName)]
            StorageMachine.freeRegister(temp1)
            StorageMachine.freeRegister(temp2)
        ret = (b,res)
    elif(binary.operation == '/'):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[idiv(res.registerName,left.registerName,right.registerName)]
        else:
            temp1 = StorageMachine.getNextTemp()
            temp2 = StorageMachine.getNextTemp()
            if(binary.leftOperand.type == 'int'):
                b+=[itof(temp1.registerName,left.registerName)]
            elif(binary.rightOperand.type == 'int'):
                b+=[itof(temp2.registerName,right.registerName)]
            b+=[fdiv(res.registerName,temp1.registerName  if (binary.leftOperand.type == 'int') else left.registerName,temp2.registerName  if (binary.rightOperand.type == 'int') else right.registerName)]
            StorageMachine.freeRegister(temp1)
            StorageMachine.freeRegister(temp2)
        ret = (b,res)
    elif(binary.operation == '%'):
        res = StorageMachine.getNextTemp()
        temp1 = StorageMachine.getNextTemp()
        temp2 = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'float'):
            b+=[ftoi(temp1.registerName,left.registerName)]
        if(binary.rightOperand.type == 'float'):
            b+=[ftoi(temp2.registerName,right.registerName)]
        b+=[imod(res.registerName,temp1.registerName  if (binary.leftOperand.type == 'float') else left.registerName,temp2.registerName if (binary.rightOperand.type == 'float') else right.registerName)]
        StorageMachine.freeRegister(temp1)
        StorageMachine.freeRegister(temp2)
        ret = (b,res)
    elif(binary.operation == '!=' or binary.operation == '=='):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[isub(res.registerName,left.registerName,right.registerName)]
        else:
            temp1 = StorageMachine.getNextTemp()
            temp2 = StorageMachine.getNextTemp()
            if(binary.leftOperand.type == 'int'):
                b+=[itof(temp1.registerName,left.registerName)]
            elif(binary.rightOperand.type == 'int'):
                b+=[itof(temp2.registerName,right.registerName)]
            b+=[fsub(res.registerName,temp1.registerName  if (binary.leftOperand.type == 'int') else left.registerName,temp2.registerName if (binary.rightOperand.type == 'int') else right.registerName)]
            StorageMachine.freeRegister(temp1)
            StorageMachine.freeRegister(temp2)
        ret = (b,res)
    elif(binary.operation == '<'):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[ilt(res.registerName,left.registerName,right.registerName)]
        else:
            temp1 = StorageMachine.getNextTemp()
            temp2 = StorageMachine.getNextTemp()
            if(binary.leftOperand.type == 'int'):
                b+=[itof(temp1.registerName,left.registerName)]
            elif(binary.rightOperand.type == 'int'):
                b+=[itof(temp2.registerName,right.registerName)]
            b+=[flt(res.registerName,temp1.registerName  if (binary.leftOperand.type == 'int') else left.registerName,temp2.registerName if (binary.rightOperand.type == 'int') else right.registerName)]
            StorageMachine.freeRegister(temp1)
            StorageMachine.freeRegister(temp2)
        ret = (b,res)
    elif(binary.operation == '<='):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[ileq(res.registerName,left.registerName,right.registerName)]
        else:
            temp1 = StorageMachine.getNextTemp()
            temp2 = StorageMachine.getNextTemp()
            if(binary.leftOperand.type == 'int'):
                b+=[itof(temp1.registerName,left.registerName)]
            elif(binary.rightOperand.type == 'int'):
                b+=[itof(temp2.registerName,right.registerName)]
            b+=[fleq(res.registerName,temp1.registerName  if (binary.leftOperand.type == 'int') else left.registerName,temp2.registerName if (binary.rightOperand.type == 'int') else right.registerName)]
            StorageMachine.freeRegister(temp1)
            StorageMachine.freeRegister(temp2)
        ret = (b,res)
    elif(binary.operation == '>'):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[igt(res.registerName,left.registerName,right.registerName)]
        else:
            temp1 = StorageMachine.getNextTemp()
            temp2 = StorageMachine.getNextTemp()
            if(binary.leftOperand.type == 'int'):
                b+=[itof(temp1.registerName,left.registerName)]
            elif(binary.rightOperand.type == 'int'):
                b+=[itof(temp2.registerName,right.registerName)]
            b+=[fgt(res.registerName,temp1.registerName  if (binary.leftOperand.type == 'int') else left.registerName,temp2.registerName if (binary.rightOperand.type == 'int') else right.registerName)]
            StorageMachine.freeRegister(temp1)
            StorageMachine.freeRegister(temp2)
        ret = (b,res)
    elif(binary.operation == '>='):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[igeq(res.registerName,left.registerName,right.registerName)]
        else:
            temp1 = StorageMachine.getNextTemp()
            temp2 = StorageMachine.getNextTemp()
            if(binary.leftOperand.type == 'int'):
                b+=[itof(temp1.registerName,left.registerName)]
            elif(binary.rightOperand.type == 'int'):
                b+=[itof(temp2.registerName,right.registerName)]
            b+=[fgeq(res.registerName,temp1.registerName  if (binary.leftOperand.type == 'int') else left.registerName,temp2.registerName if (binary.rightOperand.type == 'int') else right.registerName)]
            StorageMachine.freeRegister(temp1)
            StorageMachine.freeRegister(temp2)
        ret = (b,res)
    elif(binary.operation == '||'):
        res = StorageMachine.getNextTemp()
        b+=[iadd(res.registerName,left.registerName,right.registerName)]
        b+=[igt(res.registerName,res.registerName,curIDs['zero'].registerName)]
        ret = (b,res)
    elif(binary.operation == '&&'):
        res = StorageMachine.getNextTemp()
        two = StorageMachine.getNextTemp()
        b+=[mov_immed_i(two.registerName,2)]
        b+=[iadd(res.registerName,left.registerName,right.registerName)]
        b+=[igeq(res.registerName,res.registerName,two.registerName)]
        StorageMachine.freeRegister(two)
        ret = (b,res)

    for cell in ours:
        StorageMachine.freeRegister(cell)
    return ret

    
def processConditional(cond,labelName = "Label"):
    b = []



    tempLabel = StorageMachine.getNextLabel(labelName)
    if(cond.__class__.__name__ == 'binaryExpression_record'):
        res = processBinary(cond)
        b+=res[0]
        if(cond.operation == '=='):
            b+=[bnz(res[1].registerName,tempLabel)]
        else:
        
            b+=[bz(res[1].registerName,tempLabel)]

        StorageMachine.freeRegister(res[1])
    else:
        res = processUnary(cond)
        b+=res[0]
        b+=[bnz(res[1].registerName,tempLabel)]
        StorageMachine.freeRegister(res[1])
    return (b,tempLabel)

def handleSettingField(left,right):
    return setField(left,right)

def setField(field, value):
    b = []

    isStatic = False
    i = 0

    if field.__class__.__name__ not in ('fieldAccessExpression_record', 'methodCallExpression_record'):
        if field.__class__.__name__ == 'referenceExpression_record':
            b += [mov(value, 'a0')]
            return b

        elif field.__class__.__name__ == 'varExpression_record':
            if field.name == field.type:
                b += [mov(value, 'sap')]
                return b

        else:
            b += [mov(value, curIDs[field.id].registerName)]
            return b

    if field.__class__.__name__ == 'fieldAccessExpression_record':
        base_res = resolveFieldRecur(field.base)
        b += base_res[1]  
        base_address = base_res[0]

        for f in typeChecker.types[field.base.type].publicFields:
            if f.name == field.field:
                if getattr(f, 'applicability', None) == 'static':
                    isStatic = True
                    i = 0
                    for statField in staticFields:
                        if f.staticID == statField:
                            break
                        i += 1
                break
            i += 1

        offset = StorageMachine.getNextTemp()
        b += [mov_immed_i(offset.registerName, i)]

        if value.__class__.__name__ == 'const_record':
            temp = StorageMachine.getNextTemp()
            b += [mov_imm_cell(temp, value)]

            if isStatic:
                b += [hstore('sap', offset.registerName, temp.registerName)]
            else:
                b += [hstore(base_address, offset.registerName, temp.registerName)]
            StorageMachine.freeRegister(temp)

        elif value.__class__.__name__ == 'binaryExpression_record':
            res = processBinary(value)
            b += res[0]

            if isStatic:
                b += [hstore('sap', offset.registerName, res[1].registerName)]
            else:
                b += [hstore(base_address, offset.registerName, res[1].registerName)]

        elif value.__class__.__name__ == 'varExpression_record':

            if isStatic:
                b += [hstore('sap', offset.registerName, curIDs[value.id].registerName)]
            else:
                b += [hstore(base_address, offset.registerName, curIDs[value.id].registerName)]

        elif value.__class__.__name__ == 'unaryExpression_record':
            res = processUnary(value)
            b += res[0]

            if isStatic:
                b += [hstore('sap', offset.registerName, res[1].registerName)]
            else:
                b += [hstore(base_address, offset.registerName, res[1].registerName)]

        elif value.__class__.__name__ == 'newExpression_record':
            temp = StorageMachine.getNextTemp()

            b += [halloc(temp.registerName, typeChecker.types[value.type].typeSize())]
            b += processConstructor(temp, value)

            if isStatic:
                b += [hstore('sap', offset.registerName, temp.registerName)]
            else:
                b += [hstore(base_address, offset.registerName, temp.registerName)]

            StorageMachine.freeRegister(temp)

        elif value.__class__.__name__ == 'fieldAccessExpression_record':
            out = resolveField(value)
            b += out[1]

            if isStatic:
                b += [hstore('sap', offset.registerName, out[0])]
            else:
                b += [hstore(base_address, offset.registerName, out[0])]

        else:
            res = processMethod(value)
            b += res[0]
            if isStatic:
                b += [hstore('sap', offset.registerName, res[1].registerName)]
            else:
                b += [hstore(base_address, offset.registerName, res[1].registerName)]

        StorageMachine.freeRegister(offset)

    return b




def handleSetting(left,right):
    b = []
    
    
    if(right.__class__.__name__ == 'const_record'):
        b+=[ mov_imm_cell(left,right)]
    elif(right.__class__.__name__ == 'binaryExpression_record'):
        res = processBinary(right)
        b+= res[0]
        b+=[  mov(left.registerName,res[1].registerName)]
    elif(right.__class__.__name__ == 'varExpression_record'):

        b+=[  mov(left.registerName,curIDs[right.id].registerName)]
    elif(right.__class__.__name__ == 'unaryExpression_record'):
        res = processUnary(right)
        b+= res[0]
        b+=[  mov(left.registerName,res[1].registerName)]
    elif(right.__class__.__name__ == 'newExpression_record'):
        b+=[halloc(left.registerName,typeChecker.types[right.type].typeSize())]
        b+= processConstructor(left,right)
    elif(right.__class__.__name__ == 'fieldAccessExpression_record'):

        
        out = resolveField(right)
        b+=out[1]
        b+= [ mov(left.registerName,out[0])]
    else:
        res = processMethod(right)
        b+= res[0]
        b+=[  mov(left.registerName,res[1].registerName)]
    return b

def processExpression(exp):
    b = []
    if exp.__class__.__name__ == 'assignExpression_record':
        left = exp.assignee
        right = exp.assigner
        if(left.__class__.__name__ == 'fieldAccessExpression_record'):
            b+= handleSettingField(left,right)
        else:
            left = curIDs[left.id]
            b+= handleSetting(left,right)
        
    elif exp.__class__.__name__ == 'autoExpression_record':
        inc = StorageMachine.getNextTemp()
        out = resolveField(exp.operand)
        b+= out[1]
        if exp.auto_type == '++':
            
            if(exp.operand.type == 'int'):
                b += [iadd(out[0],out[0],curIDs['one'].registerName)]
            else:
                b+= [mov_immed_f(inc.registerName,1.0)]
                b += [fadd(out[0],out[0],inc.registerName)]
                StorageMachine.freeRegister(inc)
        else:
            if(exp.operand.type == 'int'):
                b += [isub(out[0],out[0],curIDs['one'].registerName)]
            else:
                b+= [mov_immed_f(inc.registerName,1.0)]
                b += [fsub(out[0],out[0],inc.registerName)]
                StorageMachine.freeRegister(inc)
    elif exp.__class__.__name__ == 'methodCallExpression_record':
        res = processMethod(exp)
        b+= res[0]
        out = resolveField(exp)
        b+= out[1]
        b+=[  mov(out[0],res[1].registerName)]


        
    return b

def resolveField(field):
    b = []
    if(field.__class__.__name__ != 'fieldAccessExpression_record' and field.__class__.__name__ != 'methodCallExpression_record'):
        if(field.__class__.__name__ == 'referenceExpression_record'):

            return ('a0',b)
        elif(field.__class__.__name__ == 'varExpression_record'):
            if(field.name == field.type):
                return ('sap',b)
            else:
                return (curIDs[field.id].registerName,b)
        else:
            b+=[mov(curIDs[field.id].registerName,'a0')]
            return (curIDs[field.id].registerName,b)
    temp = StorageMachine.getNextTemp()
    
    if(field.__class__.__name__ == 'fieldAccessExpression_record'):
        res = resolveFieldRecur(field.base,temp)
        offset = StorageMachine.getNextTemp()
        b+= res[1]
        i=0
        for f in typeChecker.types[field.base.type].publicFields:
        
            if f.name == field.field:
                if getattr(field, 'applicability', None) == 'static':
                    i = 0
                    for statField in staticFields:
                        if(field.staticID == statField ):
                            break
                        i+=1
                    b+= [mov_immed_i(offset.registerName,i)]
                    b+= [ hload(temp.registerName,'sap',offset.registerName)]
                    i=-1
                break
            i+=1
        if(i!=-1):
            b+=[mov_immed_i(offset.registerName,i)]
            b+=[hload(temp.registerName,res[0],offset.registerName)]
        StorageMachine.freeRegister(offset)
        
   
    
    StorageMachine.freeRegister(temp)
    return (temp.registerName,b)
    
def resolveFieldRecur(field,temp=None):
    b = []
    if(field.__class__.__name__ != 'fieldAccessExpression_record' and field.__class__.__name__ != 'methodCallExpression_record'):
        if(field.__class__.__name__ == 'referenceExpression_record'):

            return ('a0',b)
        elif(field.__class__.__name__ == 'varExpression_record'):
            if(field.name == field.type):
                return ('sap',b)
        else:
            b+=[mov(curIDs[field.id].registerName,'a0')]
            return (curIDs[field.id].registerName,b)
        
    
    if(field.__class__.__name__ == 'fieldAccessExpression_record'):
        res = resolveFieldRecur(field.base,temp)
        offset = StorageMachine.getNextTemp()
        b+=res[1]
        i=0
        for f in typeChecker.types[field.base.type].publicFields:
        
            if f.name == field.field:
                if getattr(field, 'applicability', None) == 'static':
                    i = 0
                    for statField in staticFields:
                        if(field.staticID == statField ):
                            break
                        i+=1
                    b+= [mov_immed_i(offset.registerName,i)]
                    b+= [ hload(temp.registerName,'sap',offset.registerName)]
                    i=-1
                break
            i+=1
        if(i!=-1):
            b+=[mov_immed_i(offset.registerName,i)]
            b+=[hload(temp.registerName,res[0],offset.registerName)]
        StorageMachine.freeRegister(offset)
    b+=[mov(curIDs[field.id].registerName,temp.registerName)]
    return (curIDs[field.id].registerName,b)





def processBlock(block,methodName = None,args = [], outerEnd=None,outerTop = None):
    ours = []
    b = []
    if(methodName!= None):
        b+= [label(methodName )]
    if len(args) != 0:
        temp = StorageMachine.getArgs(len(args) + 1)
        for i in range(0,len(args)):
            curIDs[args[i].ID] = temp[i+1]
            ours+=[args[i].ID]
    for line in block:
        if isinstance(line,list):
            if(line[0].__class__.__name__ == 'variable_record'):
                for var in line:
                    curIDs[var.ID] = StorageMachine.getNextTemp()
                    if(var.type == 'int'):
                        b+=[mov_immed_i(curIDs[var.ID].registerName,0)]
                    elif(var.type == 'float'):
                        b+=[mov_immed_f(curIDs[var.ID].registerName,0.0)]
                    ours += [var.ID]
        elif line.__class__.__name__ == "expressionStatement_record":
            b += processExpression(line.expression)
        elif line.__class__.__name__ == "return_record":
            if line.type != 'void':
                if(line.return_val.__class__.__name__ == 'const_record'):
                    b+=[mov_imm_cell(curIDs[returnRegister.id],line.return_val)]
                elif(line.return_val.__class__.__name__ == 'varExpression_record'):
                    b+= [mov(curIDs[returnRegister.id].registerName,curIDs[line.return_val.id].registerName)]
                elif(line.return_val.__class__.__name__ == 'binaryExpression_record'):
                    res = processBinary(line.return_val)
                    b+= res[0]
                    b+=[  mov(curIDs[returnRegister.id].registerName,res[1].registerName)]
                elif(line.return_val.__class__.__name__ == 'unaryExpression_record'):
                    res = processUnary(line.return_val)
                    
                    b+= res[0]
                    b+=[  mov(curIDs[returnRegister.id].registerName,res[1].registerName)]
                elif(line.return_val.__class__.__name__ == 'fieldAccessExpression_record'):
                    temp = StorageMachine.getNextTemp()
                    i = 0
                    for field in typeChecker.types[line.return_val.base.type].publicFields:
                        if(field.name == line.return_val.field):
                            if(field.applicability == 'static'):
                                i = 0
                                for statField in staticFields:
                                    if(field.staticID == statField ):
                                        break
                                    i+=1
                                b+= [mov_immed_i(temp.registerName,i)]
                                b+= [ hload(temp.registerName,'sap',temp.registerName)]
                                i = -1
                            break
            
                        i+=1
                    if(i!=-1):
                        b+= [mov_immed_i(temp.registerName,i)]
                        if(line.return_val.base.__class__.__name__ == 'referenceExpression_record'):
                            b+= [ hload(temp.registerName,'a0',temp.registerName)]
                        else:
                            b+= [ hload(temp.registerName,curIDs[line.return_val.base.id].registerName,temp.registerName)]
 
                else:
                    res = processMethod(line.return_val)
                    b+= res[0]
                    b+=[  mov(curIDs[returnRegister.id].registerName,res[1].registerName)]
            b += [ret()]
        elif line.__class__.__name__ == "if_record":
            tempLabel = ""
            endLabel = ""
            if(line.conditional.__class__.__name__ == 'binaryExpression_record' or
               line.conditional.__class__.__name__ == 'unaryExpression_record'):
                if(not isinstance(line.else_block,list)):
                    temp = processConditional(line.conditional, "if_else")
                else:
                    temp = processConditional(line.conditional, "if_end")
                b +=temp[0]
                tempLabel = temp[1]
                b+= processBlock(line.then_block.block)

                if(not isinstance(line.else_block,list)):
                    endLabel = StorageMachine.getNextLabel("if_end")
                    b+= [jmp(endLabel)]

                b+= [label(tempLabel)]

                if(not isinstance(line.else_block,list)):
                    b+= processBlock(line.else_block.block)

                if(endLabel!=""):
                    b+=[label(endLabel)]
            else:
                if(line.conditional.value == "true"):
                    b+= processBlock(line.then_block.block)
                #if false optimize it out

            
        elif line.__class__.__name__ == "while_record":
            tempLabel = ""
            endLabel = ""
            if(line.conditional.__class__.__name__ == 'binaryExpression_record' or
               line.conditional.__class__.__name__ == 'unaryExpression_record'):
                topLoop = StorageMachine.getNextLabel("while_top")
                endLabel = StorageMachine.getNextLabel("while_end")
                temp = processConditional(line.conditional)
                b+=[label(topLoop)]
                b +=temp[0]
                tempLabel = temp[1]

                b+= processBlock(line.loop_block.block,outerTop=topLoop,outerEnd=endLabel)
                b+= [jmp(topLoop)]

                b+= [label(tempLabel)]


                if(endLabel!=""):
                    b+=[label(endLabel)]
            else:
                if(line.conditional.value == "true"): #infinite loop but I allow it cause I'm chill like that
                    topLoop = StorageMachine.getNextLabel()
                    endLabel = StorageMachine.getNextLabel()
                    b+=[label(topLoop)]
                    
                    b+= processBlock(line.loop_block.block,outerTop=topLoop,outerEnd=endLabel)
                    b+= [jmp(topLoop)]
                    b+= [label(endLabel)] #so we can break later
                #if false optimize it out
        elif line.__class__.__name__ == "for_record":
            tempLabel = ""
            endLabel = ""
            if(line.conditional.__class__.__name__ == 'binaryExpression_record' or
               line.conditional.__class__.__name__ == 'unaryExpression_record'):
                topLoop = StorageMachine.getNextLabel("for_top")
                endLabel = StorageMachine.getNextLabel("for_post")
                b += processExpression(line.initializer.expression)
                temp = processConditional(line.conditional,"for_end")
                
                b+=[label(topLoop)]
                b +=temp[0]
                b+=processExpression(line.update_expr.expression)
                tempLabel = temp[1]

                b+= processBlock(line.loop_body.block,outerTop=topLoop,outerEnd=endLabel)
                b+= [jmp(topLoop)]

                b+= [label(tempLabel)]


                if(endLabel!=""):
                    b+=[label(endLabel)]
            else:
                if(line.conditional.value == "true"): #infinite loop but I allow it cause I'm chill like that
                    topLoop = StorageMachine.getNextLabel("for_top")
                    endLoop = StorageMachine.getNextLabel("end_loop")
                    b += processExpression(line.initializer.expression)
                    b+=[label(topLoop)]
                    b+=processExpression(line.update_expr.expression)
                    b+= processBlock(line.loop_body.block,outerTop=topLoop,outerEnd=endLoop)
                    b+= [jmp(topLoop)]
                    b+= [label(endLoop)] #so we can break later
                #if false optimize it out
        elif (line.__class__.__name__=="controlFlow_record"):
            #print("here")
            if(line.type == 'break'):
                b+=[jmp(outerEnd)]
            else:
                b+=[jmp(outerTop)]

    for id in ours:
        if(curIDs[id].registerName[0] != 'a'):
            StorageMachine.freeRegister(curIDs[id])
        del curIDs[id]
    return b

def compile(file):

    try:
        data = open(file).read()
        bonusNonsense = open('/home/gerdjunisben/Documents/CSE304/OurCompiler/src/IO.decaf').read()

        print((bonusNonsense + '\n' +  data));
        prog = parser.parse(( data), debug=False)

        blocks = []

        output = ""





        if(prog):
            static_size = 0
            for clazz in prog:
                for field in clazz.fields:
                    if(field.applicability == 'static'):
                        static_size += 1
                        global staticFields
                        staticFields += [field.staticID]
            blocks += [[halloc('sap', static_size)]]
            for clazz in prog:
                blocks += [f"# ===Class {clazz.name}==="]
                for method in clazz.methods:
                    blocks += [processBlock(method.body.block, 'M_' + method.name + '_' + str(method.ID), method.parameters)]
                for constructor in clazz.constructors:
                    blocks += [processBlock(constructor.body.block,  'C_' + str(constructor.ID), constructor.parameters) + [ret()]]
            for block in blocks:
                if isinstance(block, str):
                    output += f"{block}\n"
                    continue
                for instruction in block:
                    if isinstance(instruction, hload):
                        output += f"hload {instruction.res}, {instruction.base}, {instruction.offset}\n"
                    elif isinstance(instruction, hstore):
                        output += f"hstore {instruction.res}, {instruction.base}, {instruction.offset}\n"
                    elif isinstance(instruction, halloc):
                        output += f"halloc {instruction.register}, {instruction.cellCount}\n"
                    elif isinstance(instruction, call):
                        output += f"call {instruction.label}\n"
                    elif isinstance(instruction, jmp):
                        output += f"jmp {instruction.label}\n"
                    elif isinstance(instruction, bnz):
                        output += f"bnz {instruction.register}, {instruction.label}\n"
                    elif isinstance(instruction, bz):
                        output += f"bz {instruction.register}, {instruction.label}\n"
                    elif isinstance(instruction, fleq):
                        output += f"fleq {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, flt):
                        output += f"flt {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, fgeq):
                        output += f"fgeq {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, fgt):
                        output += f"fgt {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, fdiv):
                        output += f"fdiv {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, fmul):
                        output += f"fmul {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, fsub):
                        output += f"fsub {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, fadd):
                        output += f"fadd {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, ileq):
                        output += f"ileq {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, ilt):
                        output += f"ilt {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, igeq):
                        output += f"igeq {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, igt):
                        output += f"igt {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, imod):
                        output += f"imod {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, idiv):
                        output += f"idiv {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, imul):
                        output += f"imul {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, isub):
                        output += f"isub {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, iadd):
                        output += f"iadd {instruction.res}, {instruction.operand1}, {instruction.operand2}\n"
                    elif isinstance(instruction, restore):
                        output += f"restore {instruction.register}\n"
                    elif isinstance(instruction, save):
                        output += f"save {instruction.register}\n"
                    elif isinstance(instruction, ret):
                        output += "ret\n"
                    elif isinstance(instruction, mov):
                        output += f"move {instruction.register1}, {instruction.register2}\n"
                    elif isinstance(instruction, mov_immed_i):
                        output += f"move_immed_i {instruction.register}, {instruction.integer}\n"
                    elif isinstance(instruction, mov_immed_f):
                        output += f"move_immed_f {instruction.register}, {instruction.float}\n"
                    elif isinstance(instruction, label):
                        output += f"{instruction.name}:\n"
                    elif isinstance(instruction, ftoi):
                        output += f"ftoi {instruction.res}, {instruction.operand}\n"
                    elif isinstance(instruction, itof):
                        output += f"itof {instruction.res}, {instruction.operand}\n"
                    
                    
            return output
    except SyntaxError as e:
        print(f"Compilation failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
                
   
