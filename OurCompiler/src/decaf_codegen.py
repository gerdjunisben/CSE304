
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
    else:
        return mov_immed_f(cell.registerName,cons.value)
    

def processMethod(method):
    b =[]
    ret = None
    if(len(method.args) == 0):
        args = StorageMachine.getArgs(1)
    else:
        args = StorageMachine.getArgs(len(method.args))

    for i in range(0,len(method.args)):
        b+= handleSetting(args[i],method.args[i])
    b+= [ call(method.method_name)]
    ret = (b,args[0])

    return ret

def processConstructor(memory,newStatement):
    b =[]
    ret = None
    if(len(newStatement.args) == 0):
        args = StorageMachine.getArgs(1)
    else:
        args = StorageMachine.getArgs(len(newStatement.args) + 1)
    b+= [save(memory.registerName)]
    for i in range(0,len(newStatement.args)):
        b+= [save(args[i].registerName)]
    for i in range(0,len(newStatement.args)):
        b+= handleSetting(args[i],newStatement.args[i])
    b+= [ call(newStatement.base +  '_'+str(newStatement.id))]
    b+= [restore(memory.registerName)]
    for i in range(0,len(newStatement.args)):
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
        i = 0
        for field in typeChecker.types[binary.leftOperand.base.type].publicFields:
            if(field.name == binary.leftOperand.field):
                if(field.applicability == 'static'):
                    i = 0
                    for statField in staticFields:
                        if(field.staticID == statField ):
                            break
                        i+=1
                    b+= [mov_immed_i(left.registerName,i)]
                    b+= [ hload(left.registerName,'sap',left.registerName)]
                    i = -1
                break
            i+=1
        if ( i!= -1):
            b+= [mov_immed_i(left.registerName,i)]
            if(binary.leftOperand.base.__class__.__name__ == 'referenceExpression_record'):
                b+= [ hload(left.registerName,'a0',left.registerName)]
            else:
                b+= [ hload(left.registerName,curIDs[binary.leftOperand.base.id].registerName,left.registerName)]
    
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
        i = 0
        for field in typeChecker.types[binary.rightOperand.base.type].publicFields:
            if(field.name == binary.rightOperand.field):
                if(field.applicability == 'static'):
                    i = 0
                    for statField in staticFields:
                        if(field.staticID == statField ):
                            break
                        i+=1
                    b+= [mov_immed_i(right.registerName,i)]
                    b+= [ hload(right.registerName,'sap',right.registerName)]
                    i = -1
                break
            
            i+=1
        if(i!=-1):
            b+= [mov_immed_i(right.registerName,i)]
            if(binary.rightOperand.base.__class__.__name__ == 'referenceExpression_record'):
                b+= [ hload(right.registerName,'a0',right.registerName)]
            else:
                b+= [ hload(right.registerName,curIDs[binary.rightOperand.base.id].registerName,right.registerName)]
    else:
        res = processMethod(binary.rightOperand)
        right = res[1]
        b+= res[0]





    if(binary.operation == '+'):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[iadd(res.registerName,left.registerName,right.registerName)]
        else:
            b+=[fadd(res.registerName,left.registerName,right.registerName)]
        ret = (b,res)
    elif(binary.operation == '-'):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[isub(res.registerName,left.registerName,right.registerName)]
        else:
            b+=[fsub(res.registerName,left.registerName,right.registerName)]
        ret = (b,res)
    elif(binary.operation == '*'):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[imul(res.registerName,left.registerName,right.registerName)]
        else:
            b+=[fmul(res.registerName,left.registerName,right.registerName)]
        ret = (b,res)
    elif(binary.operation == '/'):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[idiv(res.registerName,left.registerName,right.registerName)]
        else:
            b+=[fdiv(res.registerName,left.registerName,right.registerName)]
        ret = (b,res)
    elif(binary.operation == '=='):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[isub(res.registerName,left.registerName,right.registerName)]
        else:
            b+=[fsub(res.registerName,left.registerName,right.registerName)]
        ret = (b,res)
    elif(binary.operation == '!='):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[isub(res.registerName,left.registerName,right.registerName)]
        else:
            b+=[fsub(res.registerName,left.registerName,right.registerName)]
        ret = (b,res)
    elif(binary.operation == '<'):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[ilt(res.registerName,left.registerName,right.registerName)]
        else:
            b+=[flt(res.registerName,left.registerName,right.registerName)]
        ret = (b,res)
    elif(binary.operation == '<='):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[ileq(res.registerName,left.registerName,right.registerName)]
        else:
            b+=[fleq(res.registerName,left.registerName,right.registerName)]
        ret = (b,res)
    elif(binary.operation == '>'):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[igt(res.registerName,left.registerName,right.registerName)]
        else:
            b+=[fgt(res.registerName,left.registerName,right.registerName)]
        ret = (b,res)
    elif(binary.operation == '>='):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[igeq(res.registerName,left.registerName,right.registerName)]
        else:
            b+=[fgeq(res.registerName,left.registerName,right.registerName)]
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

    
def processConditional(cond):
    b = []



    tempLabel = StorageMachine.getNextLabel()
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
    b=[]
    isStatic = False
    i = 0
    for field in typeChecker.types[left.base.type].publicFields:
        if(field.name == left.field):
            if(field.applicability == 'static'):
                isStatic = True
                i = 0
                for statField in staticFields:
                    if(field.staticID == statField ):
                        break
                    i+=1
            break
        i+=1
    offset = StorageMachine.getNextTemp()
    b+= [mov_immed_i(offset.registerName,i)]
    if(right.__class__.__name__ == 'const_record'):
        temp = StorageMachine.getNextTemp()
        b+=[ mov_imm_cell(temp,right)]

        if(isStatic):
            b+=[hstore('sap',offset.registerName,temp.registerName)]
        else:
            if(left.base.__class__.__name__ == 'referenceExpression_record'):
                b+=[hstore('a0',offset.registerName,temp.registerName)]
            else:
                b+=[hstore(curIDs[left.base.id].registerName,offset.registerName,temp.registerName)]
        StorageMachine.freeRegister(temp)
    elif(right.__class__.__name__ == 'binaryExpression_record'):
        res = processBinary(right)
        b+= res[0]
        
        if(isStatic):
            b+=[hstore('sap',offset.registerName,res[1].registerName)]
        else:
            if(left.base.__class__.__name__ == 'referenceExpression_record'):
                b+=[hstore('a0',offset.registerName,res[1].registerName)]
            else:
                b+=[hstore(curIDs[left.base.id].registerName,offset.registerName,res[1].registerName)]

    elif(right.__class__.__name__ == 'varExpression_record'):

        if(isStatic):
            b+=[hstore('sap',offset.registerName,curIDs[right.id].registerName)]
        else:
            if(left.base.__class__.__name__ == 'referenceExpression_record'):
                b+=[hstore('a0',offset.registerName,curIDs[right.id].registerName)]
            else:
                b+=[hstore(curIDs[left.base.id].registerName,offset.registerName,curIDs[right.id].registerName)]
            
    elif(right.__class__.__name__ == 'unaryExpression_record'):
        res = processUnary(right)
        b+= res[0]

        if(isStatic):
            b+=[hstore('sap',offset.registerName,res[1].registerName)]
        else:
            if(left.base.__class__.__name__ == 'referenceExpression_record'):
                b+=[hstore('a0',offset.registerName,res[1].registerName)]
            else:
                b+=[hstore(curIDs[left.base.id].registerName,offset.registerName,res[1].registerName)]

    elif(right.__class__.__name__ == 'newExpression_record'):
        temp = StorageMachine.getNextTemp()
        
        b+=[halloc(temp.registerName,typeChecker.types[right.type].typeSize())]
        b+= processConstructor(temp,right)

        if(isStatic):
            b+=[hstore('sap',offset.registerName,temp.registerName)]
        else:
            if(left.base.__class__.__name__ == 'referenceExpression_record'):
                b+=[hstore('a0',offset.registerName,temp.registerName)]
            else:
                b+=[hstore(curIDs[left.base.id].registerName,offset.registerName,temp.registerName)]

        StorageMachine.freeRegister(temp)

    elif(right.__class__.__name__ == 'fieldAccessExpression_record'):
        temp = StorageMachine.getNextTemp()
        j = 0
        for field in typeChecker.types[right.base.type].publicFields:
            if(field.name == right.field):
                if(field.applicability == 'static'):
                    j = 0
                    for statField in staticFields:
                        if(field.staticID == statField ):
                            break
                        j+=1
                    b+= [mov_immed_i(temp.registerName,i)]
                    b+= [ hload(temp.registerName,'sap',temp.registerName)]
                    return b
                break
            j+=1
        b+= [mov_immed_i(temp.registerName,i)]
        if(right.base.__class__.__name__ == 'referenceExpression_record'):
                b+=[hstore('a0',offset.registerName,temp.registerName)]
        else:
            b+=[hstore(curIDs[right.base.id].registerName,offset.registerName,temp.registerName)]
        if(isStatic):
            b+=[hstore('sap',offset.registerName,temp.registerName)]
        else:
            if(left.base.__class__.__name__ == 'referenceExpression_record'):
                b+=[hstore('a0',offset.registerName,temp.registerName)]
            else:
                b+=[hstore(curIDs[left.base.id].registerName,offset.registerName,temp.registerName)]
        StorageMachine.freeRegister(temp)
    else:
        res = processMethod(right)
        b+= res[0]
        if(isStatic):
            b+=[hstore('sap',offset.registerName,res[1].registerName)]
        else:
            b+=[hstore(curIDs[left.base.id].registerName,offset.registerName,res[1].registerName)]
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
        i = 0
        for field in typeChecker.types[right.base.type].publicFields:
            if(field.name == right.field):
                if(field.applicability == 'static'):
                    i = 0
                    for statField in staticFields:
                        if(field.staticID == statField ):
                            break
                        i+=1
                    b+= [mov_immed_i(left.registerName,i)]
                    b+= [ hload(left.registerName,'sap',left.registerName)]
                    return b
                break
            i+=1
        b+= [mov_immed_i(left.registerName,i)]
        b+= [ hload(left.registerName,curIDs[right.base.id].registerName,left.registerName)]
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
        if exp.auto_type == '++':
            if(exp.operand.type == 'int'):
                b += [iadd(curIDs[exp.operand.id].registerName,curIDs[exp.operand.id].registerName,curIDs['one'].registerName)]
            else:
                b+= [mov_immed_f(inc.registerName,1.0)]
                b += [fadd(curIDs[exp.operand.id].registerName,curIDs[exp.operand.id].registerName,inc.registerName)]
                StorageMachine.freeRegister(inc)
        else:
            if(exp.operand.type == 'int'):
                b += [isub(curIDs[exp.operand.id].registerName,curIDs[exp.operand.id].registerName,curIDs['one'].registerName)]
            else:
                b+= [mov_immed_f(inc.registerName,1.0)]
                b += [fsub(curIDs[exp.operand.id].registerName,curIDs[exp.operand.id].registerName,inc.registerName)]
                StorageMachine.freeRegister(inc)
    elif exp.__class__.__name__ == 'methodCallExpression_record':
        res = processMethod(exp.assigner)
        b+= res[0]
        b+=[  mov(curIDs[exp.assignee.id].registerName,res[1].registerName)]


        
    return b


def processBlock(block,methodName = None,args = [], outerEnd=None,outerTop = None):
    ours = []
    b = []
    if(methodName!= None):
        b+= [label(methodName)]
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
                temp = processConditional(line.conditional)
                b +=temp[0]
                tempLabel = temp[1]
                b+= processBlock(line.then_block.block)

                if(not isinstance(line.else_block,list)):
                    endLabel = StorageMachine.getNextLabel()
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
                topLoop = StorageMachine.getNextLabel()
                endLabel = StorageMachine.getNextLabel()
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
                topLoop = StorageMachine.getNextLabel()
                endLabel = StorageMachine.getNextLabel()
                b += processExpression(line.initializer.expression)
                temp = processConditional(line.conditional)
                
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
                    topLoop = StorageMachine.getNextLabel()
                    endLoop = StorageMachine.getNextLabel()
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

def check(file):


    data = open(file).read()


    prog = parser.parse(data, debug=False)

    blocks = []

    if(prog):
        static_size = 0
        for clazz in prog:
            for field in clazz.fields:
                if(field.applicability == 'static'):
                    static_size +=1
                    global staticFields
                    staticFields += [field.staticID]
        blocks += [[halloc('sap',static_size)]]
        for clazz in prog:
            for method in clazz.methods:
                blocks += [processBlock(method.body.block,method.name,method.parameters)]
            for constructor in clazz.constructors:
                blocks += [processBlock(constructor.body.block,clazz.name + '_'+ str(constructor.ID),constructor.parameters)+ [ret()]]
        for block in blocks:
            for instruction in block:
                if(isinstance(instruction,hload)):
                    print("hload " + instruction.res + ", " + instruction.base + ", " + instruction.offset )
                elif(isinstance(instruction,hstore)):
                    print("hstore " + instruction.res + ", " + instruction.base + ", " + instruction.offset )
                elif(isinstance(instruction,halloc)):
                    print("halloc " + instruction.register + ", " + str(instruction.cellCount))
                elif(isinstance(instruction,call)):
                    print("call " + instruction.label)
                elif(isinstance(instruction,jmp)):
                    print("jmp " + instruction.label )
                elif(isinstance(instruction,bnz)):
                    print("bnz " + instruction.register + ", " + instruction.label )
                elif(isinstance(instruction,bz)):
                    print("bz " + instruction.register + ", " + instruction.label )
                elif(isinstance(instruction,fleq)):
                    print("fleq " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
                elif(isinstance(instruction,flt)):
                    print("flt " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
                elif(isinstance(instruction,fgeq)):
                    print("fgeq " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
                elif(isinstance(instruction,fgt)):
                    print("fgt " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
               
                elif(isinstance(instruction,fdiv)):
                    print("fdiv " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
                elif(isinstance(instruction,fmul)):
                    print("fmul " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
                elif(isinstance(instruction,fsub)):
                    print("fsub " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
                elif(isinstance(instruction,fadd)):
                    print("fadd " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
                
                
                
                elif(isinstance(instruction,ileq)):
                    print("ileq " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
                elif(isinstance(instruction,ilt)):
                    print("ilt " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
                elif(isinstance(instruction,igeq)):
                    print("igeq " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
                elif(isinstance(instruction,igt)):
                    print("igt " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
                elif(isinstance(instruction,imod)):
                    print("imod " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
                elif(isinstance(instruction,idiv)):
                    print("idiv " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
                elif(isinstance(instruction,imul)):
                    print("imul " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
                elif(isinstance(instruction,isub)):
                    print("isub " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
                elif(isinstance(instruction,iadd)):
                    print("iadd " + instruction.res + ", " + instruction.operand1 + ", " + instruction.operand2 )
                elif(isinstance(instruction,restore)):
                    print("restore " + instruction.register  )
                elif(isinstance(instruction,save)):
                    print("save " + instruction.register )
                elif(isinstance(instruction,ret)):
                    print("ret" )
                elif(isinstance(instruction,mov)):
                    print("mov " + instruction.register1 + ", " + instruction.register2 )
                elif(isinstance(instruction,mov_immed_i)):
                    print("move_immed_i " + instruction.register + ", " + str(instruction.integer) )
                elif(isinstance(instruction,mov_immed_f)):
                    print("move_immed_f " + instruction.register + ", " + str(instruction.float) )
                elif(isinstance(instruction,label)):
                    print(instruction.name + ":"  )
                
                
                
                
                
                
    
    
    print("wala")




if __name__ == "__main__":
    sys.argv.append("OurCompiler/hw2_testing_subset/27.decaf")
    if( len(sys.argv)<2):
        print("Too few args")
        sys.exit(1)
    check(sys.argv[1])
    sys.exit(0)