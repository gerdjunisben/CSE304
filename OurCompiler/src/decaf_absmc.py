class TheStorageMachine:
    def __init__(self,regCount):

        self.tempRegSize = regCount
        self.argRegSize = regCount
        self.labelCount = 0
        
        self.argRegs = []
        for i in range(regCount):
            self.argRegs += [Cell('a' + str(i))]


        self.free = Cell('Reece')  #he manages my registers <3
        self.free.data = "sentinel"
        self.free.allocated = True
        self.free.next = self.free
        self.free.prev = self.free

        for i in range(regCount):   #I'm evil so I have this abstract sorta vm type beat
            bonus = Cell('t' + str(i))
            bonus.prev = self.free.prev
            bonus.next = self.free
            self.free.prev.next = bonus
            self.free.prev = bonus

    def getNextLabel(self):
        self.labelCount+=1;
        return "LABEL" + str(self.labelCount)

    def getArgs(self,count):
        if(count > self.argRegSize):
            raise MemoryError("Not enough arg registers")
        return self.argRegs[0:count]
    
    def getNextTemp(self):
        if self.free.next == self.free:
            raise MemoryError("No more temp registers, I'm not spilling")
        
        temp = self.free.next
        temp.allocated = True

        self.free.next = temp.next
        temp.next.prev = self.free

        temp.next = None
        temp.prev = None

        return temp
    

    def freeRegister(self,cell):
        if not isinstance(cell,Cell):
            raise ValueError("This is not a Cell dumbass") #user should never see this, only I should while debugging

        if not cell.allocated:
            raise ValueError("This cell is not allocated")
        
        cell.allocated = False

        cell.next = self.free.next
        cell.prev = self.free
        self.free.next.prev = cell
        self.free.next = cell


    def store(self,cell,value):
        self.heap[cell.cellNum] = value

    def load(self,cell):
        return self.heap[cell.cellNum]
    


    def controlStackPop(self):
        if(self.controlStackPtr==-1):
            raise IndexError("Invalid pop")
        self.controlStackPtr-=1
        return self.controlStack[self.controlStackPtr + 1]
    
    def controlStackPush(self):
        if(self.controlStackPtr== self.controlStackSize):
            raise IndexError("Invalid push, increase stack size if you need it")

class Cell:
    def __init__(self,registerName):
        self.registerName = registerName
        self.allocated = False
        self.next = None
        self.prev = None



#>>>>>>>>>>>>unneeded, thinking too smart all above probably removing soon but pretty sick though

class label():
    def __init__(self,name):
        self.name = name

class mov_immed_i():
    def __init__(self,register,integer):
        self.register = register
        self.integer = integer

class mov_immed_f():
    def __init__(self,register,float):
        self.register = register
        self.float = float


class mov():
    def __init__(self,register1,register2):
        self.register1 = register1
        self.register2 = register2


class call():
    def __init__(self,label):
        self.lable = label

class ret():
    def __init__(self):
        #pop return addr from top of control stack and return to there
        #we're not running so I guess I don't need to do anything here
        pass


class save():
    def __init__(self,register):
        self.register = register


class restore():
    def __init__(self,register):
        self.register = register


class iadd():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2

class isub():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2

class imul():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2

class idiv():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2

class imod():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2

class igt():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2

class igeq():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2

class ilt():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2


class ileq():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2


class fadd():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2

class fsub():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2

class fmul():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2

class fdiv():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2

class fmod():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2

class fgt():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2

class fgeq():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2

class flt():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2


class fleq():
    def __init__(self,res,operand1,operand2):
        self.res = res
        self.operand1 = operand1
        self.operand2 = operand2

class bz():
    def __init__(self,register,label):
        self.register = register
        self.label = label

class bnz():
    def __init__(self,register,label):
        self.register = register
        self.label = label


class jmp():
    def __init__(self,label):
        self.label = label