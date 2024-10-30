# Benjamin Gerdjunis 
# SB ID: 115962358
# Net ID: bgerdjunis
# Donato Zampini
# SB ID: 114849209
# Net ID: dzampini


import decaf_lexer as lexer
import decaf_parser as parser
import sys





#>>>>>>>>>>>>>>>>>>>>>> Record classes <<<<<<<<<<<<<<<<<<<<<<<<<



class class_record:
    def __init__(self, name,superName,constructors,methods,fields):
        self.name = name
        self.superName = superName
        self.constructors = constructors #Set of all constructors defined in class
        self.methods = methods #Set of all methods defined in class
        self.fields = fields #Set of all fields defind in class

class constructor_record:
    constructID = 0
    def __init__(self, visibility, parameters, variable_table, body):
        self.visibility = visibility
        self.parameters = parameters #Sequence of parameters, each parameter is a variable in variable table
        self.variable_table = variable_table #Table of all variables
        self.body = body #Instance of statement record
        self.ID = constructor_record.constructID
        constructor_record.constructID += 1

class method_record:
    methodID =0
    def __init__(self,name,className,visibility,applicability,parameters,returnType,variable_table,body):
        self.name = name
        self.className = className
        self.visiblity = visibility
        self.applicability = applicability
        self.parameters = parameters
        self.returnType = returnType
        self.variable_table = variable_table
        self.body = body
        self.ID = method_record.methodID
        method_record.methodID +=1

class field_record:
    fieldID = 0
    def __init__(self, name, className, visibility, applicability, type):
        self.name = name
        self.className = className
        self.visibility = visibility
        self.applicability = applicability
        self.type = type
        self.ID = field_record.fieldID
        field_record.fieldID += 1



class variable_record:
    varID = 0
    def __init__(self,name,kind,type):
        self.name = name
        self.kind = kind  #local or formal <3
        self.type = type
        self.ID = variable_record.varID
        variable_record.varID +=1



#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Statement records
class statement_record:  #This exists so that we can easily check instance
    def __init__(self):
        pass


class if_record(statement_record):
    def __init__(self,conditional,then_block,else_block):
        super().__init__()  #this line calls the super constructor which lets us do isinstance on an if to check if it's a statement
        self.conditional = conditional
        self.then_block = then_block
        self.else_block = else_block

class while_record(statement_record):
    def __init__(self,conditional,loop_block):
        super().__init__()  
        self.conditional = conditional
        self.loop_block = loop_block

class for_record(statement_record):
    def __init__(self,initializer,conditional,update_expr,loop_body):
        super().__init__()  
        self.initializer = initializer
        self.conditional = conditional
        self.update_expr = update_expr
        self.loop_body = loop_body

class return_record(statement_record):
    def __init__(self,return_val):
        super().__init__()  
        self.return_val = return_val

class expressionStatement_record(statement_record):
    def __init__(self,expression):
        super().__init__()  
        self.expression = expression

class block_record(statement_record):
    def __init__(self,block):
        super().__init__()  
        self.block = block

class controlFlow_record(statement_record):
    def __init__(self,type):
        super().__init__()  
        self.type = type

#>>>>>>>>>>>>>>>>>>>>>>>>>Expression records
class expression_record:  #This exists so that we can easily check instance
    def __init__(self):
        pass

class const_record(expression_record):
    def __init__(self,type,value):
        super().__init__()  
        self.type = type
        self.value = value

class varExpression_record(expression_record):
    def __init__(self,name,id):   #ID needs to be filled in after parsing
        super().__init__()  
        self.name = name
        self.id = id

class unaryExpression_record(expression_record):
    def __init__(self,operation,operand):  
        super().__init__()  
        self.operand = operand
        self.operation = operation

class binaryExpression_record(expression_record):
    def __init__(self,leftOperand,operation,rightOperand): 
        super().__init__()  
        self.leftOperand = leftOperand
        self.operation = operation
        self.rightOperand = rightOperand

class assignExpression_record(expression_record):
    def __init__(self,assignee,assigner):  
        super().__init__()  
        self.assignee = assignee
        self.assigner = assigner

class autoExpression_record(expression_record):
    def __init__(self,operand,auto_type,tense):  
        super().__init__() 
        self.operand = operand
        self.auto_type = auto_type
        self.tense = tense

class fieldAccessExpression_record(expression_record):
    def __init__(self,base,field):  
        super().__init__()  
        self.base = base
        self.field = field

class methodCallExpression_record(expression_record):
    def __init__(self,base,method_name,args):  
        super().__init__()  
        self.base = base
        self.method_name = method_name
        self.args = args

class newExpression_record(expression_record):
    def __init__(self,base,args):  
        super().__init__()  
        self.base = base
        self.args = args

class referenceExpression_record(expression_record):
    def __init__(self,ref_type):  
        super().__init__()  
        self.ref_type = ref_type


#>>>>>>>>>>>>>>>>>>>>>>make base library stuffs<<<<<<<<<<<<<<<<<<<


#<<<<<<<<<<<<<<<<<In>>>>>>>>>>>>>>>>>>>>
scan_int = method_record("scan_int","In","public","static",None,"int",None,None)
scan_float = method_record("scan_float","In","public","static",None,"float",None,None)
In = class_record("In",None,None,[scan_int,scan_float],None)


#<<<<<<<<<<<<<<<<Out>>>>>>>>>>>>>>>>>>>>>>
t1_print = method_record("print","Out","public","static",[variable_record("i","formal","int")],None,None,None)
t2_print = method_record("print","Out","public","static",[variable_record("f","formal","float")],None,None,None)
t3_print = method_record("print","Out","public","static",[variable_record("b","formal","boolean")],None,None,None)
t4_print = method_record("print","Out","public","static",[variable_record("s","formal","string")],None,None,None)
Out = class_record("Out",None,None,[t1_print,t2_print,t3_print,t4_print],None)

#>>>>>>>>>>>>>>>>>>>>>>data structures<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class_table = [In,Out]
method_table = [scan_int,scan_float,t1_print,t2_print,t3_print,t4_print]



#>>>>>>>>>>>>>>>>>>>>>Turn parse tree into needed classes<<<<<<<<<<<<<<<<<<<,,,
def check(file):


    data = open(file).read()



    prog = parser.parse(data, debug=False)




    #Shitty printer to make sure what I think is happening is happening, use for inspiration
    if(prog):
        print(prog)
        for clazz in prog:
            print(">>>>>>>>>>CLASS<<<<<<<<<<<<,")
            print(vars(clazz))
            print(">>>>>>>>>>>>constructors")
            for const in clazz.constructors:
                print(vars(const))
            print(">>>>>>>>>>>>methods")
            for method in clazz.methods:
                print(vars(method))
            print(">>>>>>>>>>>>>fields")
            for field in clazz.fields:
                print(vars(field))
        
        return 1
    return 0



if __name__ == "__main__":
    if( len(sys.argv)<2):
        print("Too few args")
        sys.exit(1)
    check(sys.argv[1])
    sys.exit(0)





#>>>>>>>>>>>>>>>>>>>>print out of classes data structure<<<<<<<<<<<<<<<<<<

