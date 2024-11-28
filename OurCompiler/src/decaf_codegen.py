
import decaf_parser as parser
import sys
from decaf_absmc import *

StorageMachine = TheStorageMachine(100)


curIDs = {'return':StorageMachine.getArgs(1)[0]}

class ReturnRegister:
    def __init__(self):
        self.id = 'return'



returnRegister = ReturnRegister()

def mov_imm(reg,cons):
    if(cons.type == 'int'):
        return mov_immed_i(curIDs[reg.id].registerName,cons.value)
    else:
        return mov_immed_f(curIDs[reg.id].registerName,cons.value)
    
def mov_imm_temp(cell,cons):
    if(cons.type == 'int'):
        return mov_immed_i(cell.registerName,cons.value)
    else:
        return mov_immed_f(cell.registerName,cons.value)
    
def processArithmetic(binary):
    b = []
    ours = []
    ret = None
    if(binary.leftOperand.__class__.__name__ == 'const_record'):
        left = StorageMachine.getNextTemp()
        ours +=[left]
        b+=[mov_imm_temp(left,binary.leftOperand)]
    elif(binary.leftOperand.__class__.__name__ == 'varExpression_record'):
        left = curIDs[binary.leftOperand.id]
    else:
        res =processArithmetic(binary.leftOperand)
        b += res[0]
        left = res[1]
        ours +=[left]



    if(binary.rightOperand.__class__.__name__ == 'const_record'):
        right = StorageMachine.getNextTemp()
        ours +=[right]
        b+=[mov_imm_temp(right,binary.rightOperand)]
    elif(binary.rightOperand.__class__.__name__ == 'varExpression_record'):
        right = curIDs[binary.rightOperand.id]
    else:
        res = processArithmetic(binary.rightOperand)
        b += res[0]
        right = res[1]
        ours +=[right]

    if(binary.operation == '+'):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[iadd(res.registerName,left.registerName,right.registerName)]
        else:
            b+=[fadd(res.registerName,left.registerName,right.registerName)]
        ret = (b,res)

    for cell in ours:
        StorageMachine.freeRegister(cell)
    return ret

    
def processBinary(binary):
    b = []
    ours = []
    left = None
    right = None

    if(binary.leftOperand.__class__.__name__ == 'const_record'):
        left = StorageMachine.getNextTemp()
        ours +=[left]
        b+=[mov_imm_temp(left,binary.leftOperand)]
    elif(binary.leftOperand.__class__.__name__ == 'varExpression_record'):
        left = curIDs[binary.leftOperand.id]
    else:
        res = processArithmetic(binary.leftOperand)
        left = res[1]
        ours +=[left]
        b+= res[0]



    if(binary.rightOperand.__class__.__name__ == 'const_record'):
        right = StorageMachine.getNextTemp()
        ours +=[right]
        b+=[mov_imm_temp(right,binary.rightOperand)]
    elif(binary.rightOperand.__class__.__name__ == 'varExpression_record'):
        right = curIDs[binary.rightOperand.id]
    else:
        res = processArithmetic(binary.rightOperand)
        right = res[1]
        ours +=[right]
        b+= res[0]



    tempLabel = None
    if(binary.operation == '=='):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[isub(res.registerName,left.registerName,right.registerName)]
        else:
            b+=[fsub(res.registerName,left.registerName,right.registerName)]
        tempLabel = StorageMachine.getNextLabel()
        b+=[bnz(res.registerName,tempLabel)]
        StorageMachine.freeRegister(res)
    elif(binary.operation == '<'):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[ilt(res.registerName,left.registerName,right.registerName)]
        else:
            b+=[flt(res.registerName,left.registerName,right.registerName)]
        tempLabel = StorageMachine.getNextLabel()
        b+=[bz(res.registerName,tempLabel)]
        StorageMachine.freeRegister(res)
    elif(binary.operation == '<='):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[ileq(res.registerName,left.registerName,right.registerName)]
        else:
            b+=[fleq(res.registerName,left.registerName,right.registerName)]
        tempLabel = StorageMachine.getNextLabel()
        b+=[bz(res.registerName,tempLabel)]
        StorageMachine.freeRegister(res)
    elif(binary.operation == '>'):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[igt(res.registerName,left.registerName,right.registerName)]
        else:
            b+=[fgt(res.registerName,left.registerName,right.registerName)]
        tempLabel = StorageMachine.getNextLabel()
        b+=[bz(res.registerName,tempLabel)]
        StorageMachine.freeRegister(res)
    elif(binary.operation == '>='):
        res = StorageMachine.getNextTemp()
        if(binary.leftOperand.type == 'int' and binary.rightOperand.type == 'int'):
            b+=[igeq(res.registerName,left.registerName,right.registerName)]
        else:
            b+=[fgeq(res.registerName,left.registerName,right.registerName)]
        tempLabel = StorageMachine.getNextLabel()
        b+=[bz(res.registerName,tempLabel)]
        StorageMachine.freeRegister(res)
    for cell in ours:
        StorageMachine.freeRegister(cell)
    return (b,tempLabel)

def processExpression(exp):
    b = []
    if exp.__class__.__name__ == 'assignExpression_record':
        if(exp.assigner.__class__.__name__ == 'const_record'):
            b+=[ mov_imm(exp.assignee,exp.assigner)]
        else:
            b+=[  mov(curIDs[exp.assignee.id].registerName,curIDs[exp.assigner.id].registerName)]
    elif exp.__class__.__name__ == 'autoExpression_record':
        inc = StorageMachine.getNextTemp()
        b+= [mov_immed_i(inc.registerName,1)]
        if exp.auto_type == '++':
            if(exp.operand.type == 'int'):
                b += [iadd(curIDs[exp.operand.id].registerName,curIDs[exp.operand.id].registerName,inc.registerName)]
            else:
                b += [fadd(curIDs[exp.operand.id].registerName,curIDs[exp.operand.id].registerName,inc.registerName)]
        else:
            if(exp.operand.type == 'int'):
                b += [isub(curIDs[exp.operand.id].registerName,curIDs[exp.operand.id].registerName,inc.registerName)]
            else:
                b += [fsub(curIDs[exp.operand.id].registerName,curIDs[exp.operand.id].registerName,inc.registerName)]
        StorageMachine.freeRegister(inc)
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
                else:
                    b+= [mov(curIDs[returnRegister.id].registerName,curIDs[line.return_val.id].registerName)]
            b += [ret()]
        elif line.__class__.__name__ == "if_record":
            tempLabel = ""
            endLabel = ""
            if(line.conditional.__class__.__name__ == 'binaryExpression_record'):
                temp = processBinary(line.conditional)
                b +=temp[0]
                tempLabel = temp[1]
            else:
                pass

            b+= processBlock(line.then_block.block)

            if(not isinstance(line.else_block,list)):
                endLabel = StorageMachine.getNextLabel()
                b+= [jmp(endLabel)]

            b+= [label(tempLabel)]

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