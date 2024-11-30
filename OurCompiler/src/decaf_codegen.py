
import decaf_parser as parser
import sys
from decaf_absmc import *

StorageMachine = TheStorageMachine(100)


curIDs = {'return':StorageMachine.getArgs(1)[0],'one':StorageMachine.getNextTemp(),'zero':StorageMachine.getNextTemp()}

class ReturnRegister:
    def __init__(self):
        self.id = 'return'



returnRegister = ReturnRegister()

def mov_imm(reg,cons):
    if(cons.type == 'int'):
        return mov_immed_i(curIDs[reg.id].registerName,cons.value)
    else:
        return mov_immed_f(curIDs[reg.id].registerName,cons.value)
    
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
        b+= handleExpression(args[i],method.args[i])
    b+= [ call(method.method_name)]
    ret = (b,args[0])

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
    elif(left.__class__.__name__ == 'binaryExpression_record'):
        res = processBinary(binary.leftOperand)
        left = res[1]
        ours +=[left]
        b+= res[0]
    else:
        res = processMethod(binary.leftOperand)
        left = res[1]
        ours +=[left]
        b+= res[0]


    if(binary.rightOperand.__class__.__name__ == 'const_record'):
        right = StorageMachine.getNextTemp()
        ours +=[right]
        b+=[mov_imm_cell(right,binary.rightOperand)]
    elif(binary.rightOperand.__class__.__name__ == 'varExpression_record'):
        right = curIDs[binary.rightOperand.id]
    elif(right.__class__.__name__ == 'binaryExpression_record'):
        res = processBinary(binary.rightOperand)
        right = res[1]
        ours +=[right]
        b+= res[0]
    else:
        res = processMethod(binary.rightOperand)
        right = res[1]
        ours +=[right]
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

    
def processConditional(binary):
    b = []



    tempLabel = StorageMachine.getNextLabel()
    res = processBinary(binary)
    b+=res[0]
    if(binary.operation == '=='):
        b+=[bnz(res[1].registerName,tempLabel)]
    else:
        
        b+=[bz(res[1].registerName,tempLabel)]

    StorageMachine.freeRegister(res[1])
    return (b,tempLabel)

def handleExpression(left,right):
    b = []
    if(right.__class__.__name__ == 'const_record'):
        b+=[ mov_imm_cell(left,right)]
    elif(right.__class__.__name__ == 'binaryExpression_record'):
        res = processBinary(right)
        b+= res[0]
        b+=[  mov(left.registerName,res[1].registerName)]
    elif(right.__class__.__name__ == 'varExpression_record'):

        b+=[  mov(left.registerName,curIDs[right.id].registerName)]
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
        left = curIDs[left.id]
        b+= handleExpression(left,right)
        
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


def processBlock(block,methodName = None,args = None):
    ours = []
    b = []
    if(methodName!= None):
        b+= [label(methodName)]
    if args!=None:
        temp = StorageMachine.getArgs(len(args))
        for i in range(0,len(args)):
            curIDs[args[i].ID] = temp[i]
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
                    b+=[mov_imm(returnRegister,line.return_val)]
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
            if(line.conditional.__class__.__name__ == 'binaryExpression_record'):
                temp = processConditional(line.conditional)
                b +=temp[0]
                tempLabel = temp[1]
            else:
                pass

            b+= processBlock(line.then_block.block)

            if(not isinstance(line.else_block,list)):
                endLabel = StorageMachine.getNextLabel()
                b+= [jmp(endLabel)]

            b+= [label(tempLabel)]

            if(not isinstance(line.else_block,list)):
                b+= processBlock(line.else_block.block)

            if(endLabel!=""):
                b+=[label(endLabel)]

    for id in ours:
        StorageMachine.freeRegister(curIDs[id])
        del curIDs[id]
    return b

def check(file):


    data = open(file).read()


    prog = parser.parse(data, debug=False)
    if not isinstance(prog,tuple):
        prog = (prog,)

    blocks = []

    if(prog):
        for clazz in prog:
            for method in clazz.methods:
                blocks += [processBlock(method.body.block,method.name,method.parameters)]

    print("wala")




if __name__ == "__main__":
    sys.argv.append("OurCompiler/hw2_testing_subset/27.decaf")
    if( len(sys.argv)<2):
        print("Too few args")
        sys.exit(1)
    check(sys.argv[1])
    sys.exit(0)