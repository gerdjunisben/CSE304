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
    def __init__(self, name,superName,constructors,methods,fields,line):
        self.name = name
        self.superName = superName
        self.constructors = constructors #Set of all constructors defined in class
        self.methods = methods #Set of all methods defined in class
        self.fields = fields #Set of all fields defind in class
        self.line = line

class constructor_record:
    constructID = 0
    def __init__(self, visibility, parameters, variable_table, body,line):
        self.visibility = visibility
        self.parameters = parameters #Sequence of parameters, each parameter is a variable in variable table
        self.variable_table = variable_table #Table of all variables
        self.body = body #Instance of statement record
        self.line = line
        self.ID = constructor_record.constructID
        constructor_record.constructID += 1

class method_record:
    methodID =0
    def __init__(self,name,className,visibility,applicability,parameters,returnType,variable_table,body,line):
        self.name = name
        self.className = className
        self.visibility = visibility
        self.applicability = applicability
        self.parameters = parameters
        self.returnType = returnType
        self.variable_table = variable_table
        self.body = body
        self.line = line
        self.ID = method_record.methodID
        method_record.methodID +=1

class field_record:
    fieldID = 0
    def __init__(self, name, className, visibility, applicability, type,line):
        self.name = name
        self.className = className
        self.visibility = visibility
        self.applicability = applicability
        self.type = type
        self.line = line
        self.ID = field_record.fieldID
        field_record.fieldID += 1



class variable_record:
    varID = 0
    def __init__(self,name,kind,type,line):
        self.name = name
        self.kind = kind  #local or formal <3
        self.type = type
        self.line = line
        self.ID = variable_record.varID
        variable_record.varID +=1



#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Statement records
class statement_record(object):  #This exists so that we can easily check instance
    def __init__(self,line):
        self.line = line
        pass


class if_record(statement_record):
    def __init__(self,conditional,then_block,else_block,line):
        super().__init__(line)  #this line calls the super constructor which lets us do isinstance on an if to check if it's a statement
        self.conditional = conditional
        self.then_block = then_block
        self.else_block = else_block

class while_record(statement_record):
    def __init__(self,conditional,loop_block,line):
        super().__init__(line) 
        self.conditional = conditional
        self.loop_block = loop_block

class for_record(statement_record):
    def __init__(self,initializer,conditional,update_expr,loop_body,line):
        super().__init__(line) 
        self.initializer = initializer
        self.conditional = conditional
        self.update_expr = update_expr
        self.loop_body = loop_body

class return_record(statement_record):
    def __init__(self,return_val,line):
        super().__init__(line)  
        self.return_val = return_val

class expressionStatement_record(statement_record):
    def __init__(self,expression,line):
        super().__init__(line) 
        self.expression = expression

class block_record(statement_record):
    def __init__(self,block,variable_table,line):
        super().__init__(line) 
        self.block = block
        self.variable_table = variable_table

class controlFlow_record(statement_record):
    def __init__(self,type,line):
        super().__init__(line) 
        self.type = type

#>>>>>>>>>>>>>>>>>>>>>>>>>Expression records
class expression_record(object):  #This exists so that we can easily check instance
    def __init__(self,line):
        self.line = line
        pass

class const_record(expression_record):
    def __init__(self,type,value,line):
        super().__init__(line) 
        self.type = type
        self.value = value

class varExpression_record(expression_record):
    def __init__(self,name,id,line):   #ID needs to be filled in after parsing
        super().__init__(line)  
        self.name = name
        self.id = id

class unaryExpression_record(expression_record):
    def __init__(self,operation,operand,line):  
        super().__init__(line) 
        self.operand = operand
        self.operation = operation

class binaryExpression_record(expression_record):
    def __init__(self,leftOperand,operation,rightOperand,line): 
        super().__init__(line) 
        self.leftOperand = leftOperand
        self.operation = operation
        self.rightOperand = rightOperand

class assignExpression_record(expression_record):
    def __init__(self,assignee,assigner,line):  
        super().__init__(line) 
        self.assignee = assignee
        self.assigner = assigner

class autoExpression_record(expression_record):
    def __init__(self,operand,auto_type,tense,line):  
        super().__init__(line) 
        self.operand = operand
        self.auto_type = auto_type
        self.tense = tense

class fieldAccessExpression_record(expression_record):
    def __init__(self,base,field,line):  
        super().__init__(line) 
        self.base = base
        self.field = field

class methodCallExpression_record(expression_record):
    def __init__(self,base,method_name,args,line):  
        super().__init__(line) 
        self.base = base
        self.method_name = method_name
        self.args = args

class newExpression_record(expression_record):
    def __init__(self,base,args,line):  
        super().__init__(line) 
        self.base = base
        self.args = args

class referenceExpression_record(expression_record):
    def __init__(self,ref_type,line):  
        super().__init__(line) 
        self.ref_type = ref_type


#>>>>>>>>>>>>>>>>>>>>>>make base library stuffs<<<<<<<<<<<<<<<<<<<


#<<<<<<<<<<<<<<<<<In>>>>>>>>>>>>>>>>>>>>
scan_int = method_record("scan_int","In","public","static",None,"int",None,None,0)
scan_float = method_record("scan_float","In","public","static",None,"float",None,None,0)
In = class_record("In",None,None,[scan_int,scan_float],None,0)


#<<<<<<<<<<<<<<<<Out>>>>>>>>>>>>>>>>>>>>>>
t1_print = method_record("print","Out","public","static",[variable_record("i","formal","int",0)],None,None,None,0)
t2_print = method_record("print","Out","public","static",[variable_record("f","formal","float",0)],None,None,None,0)
t3_print = method_record("print","Out","public","static",[variable_record("b","formal","boolean",0)],None,None,None,0)
t4_print = method_record("print","Out","public","static",[variable_record("s","formal","string",0)],None,None,None,0)
Out = class_record("Out",None,None,[t1_print,t2_print,t3_print,t4_print],None,0)

#>>>>>>>>>>>>>>>>>>>>>>data structures<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class_table = [In,Out]
method_table = [scan_int,scan_float,t1_print,t2_print,t3_print,t4_print]
field_table = []
constructor_table = []



#>>>>>>>>>>>>>>>>>>>>>Turn parse tree into needed classes<<<<<<<<<<<<<<<<<<<,,,
def check(file):


    data = open(file).read()



    prog = parser.parse(data, debug=False)
    
    for item in prog:
        class_table.append(item)


    for classes in prog:
        class_table.append(classes)
        for methods in classes.methods:
            method_table.append(methods)
    #Check for duplicate classes
    class_set = set(class_table)
    if(len(class_set) != len(class_table)):
        print("Error, duplicate class name")
        return -1
    
    #Check for duplicate methods
    counter = 1
    length = len(method_table)
    # for methods in method_table:
    #     print(str(vars(methods))+"\n")
    for methods in method_table:
        name = methods.name
        params = methods.parameters
        class1 = methods.className
        line = methods.line
        for i in range(counter, length):
            if(name == method_table[i].name and class1 == method_table[i].className and params == method_table[i].parameters):
                print("Error, invalid method.\nMethod is "+name+" in class "+class1+" at line "+str(line)+".\nMethod has duplicate name, class, and parameters.")
                return -2
        counter += 1


    #Shitty printer to make sure what I think is happening is happening, use for inspiration
    if(prog):
        print(prog)
        for clazz in prog:
            print(">>>>>>>>>>CLASS<<<<<<<<<<<<,")
            print(vars(clazz))
            print(">>>>>>>>>>>>constructors")
            for const in clazz.constructors:
                print(vars(const))
                print("==========BODY========")
                for line in const.body:
                    print(type(line))
                    if line!=None:
                        print(vars(line))
                print("==========BODY========")
            print(">>>>>>>>>>>>methods")
            for method in clazz.methods:
                print(vars(method))
                print("==========BODY========")
                for line in const.body:
                    print(type(line))
                    if line!=None:
                        print(vars(line))
                print("==========BODY========")
            print(">>>>>>>>>>>>>fields")
            for field in clazz.fields:
                print(vars(field))
        
        return 1
    return 0

    # Real printer
    if(prog):
        for clazz in class_table:
            print("-------------------------------------------------------------------------")
            print("- Class Name:"+clazz.name)
            print("Superclass Name:"+str(clazz.superName))
            print("Fields:")
            if(clazz.fields):
                for field in clazz.fields:
                    print(str(field))
            print("Constructors:")
            if(clazz.constructors):
                for constructor in clazz.constructors:
                    print("CONSTRUCTOR: "+str(constructor.ID)+", "+str(constructor.visibility))
                    print("Variable Table:\n"+str(constructor.variable_table))
                    print("Constructor Body:\n"+str(constructor.body))
            print("Methods:")
            if(clazz.methods):
                for method in clazz.methods:
                    print("METHOD: "+str(method.ID)+", "+method.name+", "+method.className+", "+str(method.visibility)+", "+str(method.applicability)+", "+str(method.returnType))
                    print("Method Parameters:")
                    if(method.parameters):
                        for param in method.parameters:
                            print(str(param))
                    print("Variable Table:")
                    if(method.variable_table):
                        print(str(method.variable_table))
                    if(method.body):
                        print("Block"+str(method.body))


if __name__ == "__main__":
    if( len(sys.argv)<2):
        print("Too few args")
        sys.exit(1)
    check(sys.argv[1])
    sys.exit(0)





#>>>>>>>>>>>>>>>>>>>>print out of classes data structure<<<<<<<<<<<<<<<<<<

