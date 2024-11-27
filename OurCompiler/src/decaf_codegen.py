
import decaf_parser as parser
import sys
from decaf_absmc import *

StorageMachine = TheStorageMachine(100)


curIDs = {}

def processExpression(exp):
    if exp.__class__.__name__ == 'assignExpression_record':
        if(exp.assigner.__class__.__name__ == 'const_record'):
            if(exp.assigner.type == 'int'):
                return mov_immed_i(curIDs[exp.assignee.id].registerName,exp.assigner.value)
            else:
                return mov_immed_f(curIDs[exp.assignee.id].registerName,exp.assigner.value)
        else:
            return mov(curIDs[exp.assignee.id].registerName,curIDs[exp.assigner.id].registerName)

def processBlock(block,methodName):
    ours = []
    b = []
    b+= [label(methodName)]
    for line in block:
        if isinstance(line,list):
            if(line[0].__class__.__name__ == 'variable_record'):
                for var in line:
                    curIDs[var.ID] = StorageMachine.getNextTemp()
                    ours += [var.ID]
        elif line.__class__.__name__ == "expressionStatement_record":
            b += [processExpression(line.expression)]
    b+= [ret()]
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
                blocks += [processBlock(method.body.block,method.name)]

    print("wala")




if __name__ == "__main__":
    sys.argv.append("OurCompiler/hw2_testing_subset/27.decaf")
    if( len(sys.argv)<2):
        print("Too few args")
        sys.exit(1)
    check(sys.argv[1])
    sys.exit(0)