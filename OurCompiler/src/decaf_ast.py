# Benjamin Gerdjunis 
# SB ID: 115962358
# Net ID: bgerdjunis
# Donato Zampini
# SB ID: 114849209
# Net ID: dzampini


import decaf_lexer as lexer
import decaf_parser as parser
import sys
from decaf_lexer import global_symbol_table
from decaf_typecheck import typeChecker




#>>>>>>>>>>>>>>>>>>>>>> Record classes <<<<<<<<<<<<<<<<<<<<<<<<<



class class_record:
    def __init__(self, name,superName,constructors,methods,fields,body,line):
        self.name = name
        self.superName = superName
        self.constructors = constructors #Set of all constructors defined in class
        self.methods = methods #Set of all methods defined in class
        self.fields = fields #Set of all fields defind in class
        self.body = body
        self.line = line
        global_symbol_table.addParams()
        #print(str(line) + "," + str(global_symbol_table.cur.names))
        self.miniName = global_symbol_table.exitScope()
        if(superName==None):
            typeChecker.addUsertype(name,'object',self.miniName)
        else:
            typeChecker.addUsertype(name,superName,self.miniName)
        global_symbol_table.setRefs(self.name)
        global_symbol_table.setID(name,-1)
        global_symbol_table.executeFieldLookUps()

class constructor_record:
    constructID = 1
    def __init__(self,className, visibility, parameters, variable_table, body,line):
        self.visibility = visibility
        self.parameters = parameters #Sequence of parameters, each parameter is a variable in variable table
        self.variable_table = variable_table #Table of all variables
        if body!=None:
            self.variable_table+= body.variable_table
        self.body = body #Instance of statement record
        self.line = line
        self.ID = constructor_record.constructID
        global_symbol_table.setIDConst(className,(self,self.ID))

        constructor_record.constructID += 1

class method_record:
    methodID =1
    def __init__(self,name,className,visibility,applicability,parameters,returnType,variable_table,body,line):
        self.name = name
        self.className = className
        self.visibility = visibility
        self.applicability = applicability
        self.parameters = parameters
        self.returnType = returnType
        self.variable_table = variable_table 
        if body!=None:
            self.variable_table+= body.variable_table
        self.body = body
        self.line = line
        self.ID = method_record.methodID
        global_symbol_table.setID(name,(self,self.ID))
        method_record.methodID +=1

class field_record:
    fieldID = 1
    def __init__(self, name, className, visibility, applicability, type,line):
        self.name = name
        self.className = className
        self.visibility = visibility
        self.applicability = applicability
        self.type = type
        self.line = line
        self.ID = field_record.fieldID
        global_symbol_table.setID(name,(self,self.ID))
        global_symbol_table.removeParam(name)
        field_record.fieldID += 1



class variable_record:
    varID = 1
    def __init__(self,name,kind,type,line):
        self.name = name
        self.kind = kind  #local or formal <3
        self.type = type
        self.line = line
        self.ID = variable_record.varID
        global_symbol_table.recordParam(name,(self,self.ID))
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
        global_symbol_table.addParams()
        self.variable_table = variable_table + global_symbol_table.returnAllVars()
        #print(self.variable_table)
        self.miniName = global_symbol_table.exitScope()
        variable_record.varID=1

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
    def __init__(self,name,line):   #ID needs to be filled in after parsing
        super().__init__(line)  
        self.name = name
        lookup = global_symbol_table.lookUp(name)
        #print(lookup)
        self.id = lookup[1]
        self.type = lookup[0]

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
        global_symbol_table.executeFieldLookUps()
        res = typeChecker.checkValid(operand,{'int','float'})
        if(res != None):
            self.type = res
        else:
            self.type = 'error'
        self.operand = operand
        self.auto_type = auto_type
        self.tense = tense

class fieldAccessExpression_record(expression_record):
    def __init__(self,base,field,line):  
        super().__init__(line) 
        self.base = base
        self.field = field
        #returns -1 if invalid
        global_symbol_table.addFieldLookUp(base,field,self)

class methodCallExpression_record(expression_record):
    def __init__(self,fieldAccess,args,line):  
        super().__init__(line) 
        self.base = fieldAccess.base
        self.method_name = fieldAccess.field
        if(not isinstance(args,list)):
            args = [args]
        self.args = args
        global_symbol_table.addArgs(fieldAccess,args)

class newExpression_record(expression_record):
    def __init__(self,base,args,line):  
        super().__init__(line) 
        self.base = base
        self.args = args
        global_symbol_table.addFieldLookUp(base,base,self)
        global_symbol_table.addArgs(self,args)

class referenceExpression_record(expression_record):
    def __init__(self,ref_type,line):  
        super().__init__(line) 
        self.ref_type = ref_type
        self.className = None
        global_symbol_table.addRef(self)


#>>>>>>>>>>>>>>>>>>>>>>make base library stuffs<<<<<<<<<<<<<<<<<<<


#<<<<<<<<<<<<<<<<<In>>>>>>>>>>>>>>>>>>>>
'''
global_symbol_table.enterNewScope()
scan_int = method_record("scan_int","In","public","static",None,"int",None,None,0)
scan_float = method_record("scan_float","In","public","static",None,"float",None,None,0)
In = class_record("In",None,None,[scan_int,scan_float],None,[],0)
'''

#<<<<<<<<<<<<<<<<Out>>>>>>>>>>>>>>>>>>>>>>
'''
global_symbol_table.enterNewScope()
t1_print = method_record("print","Out","public","static",[variable_record("i","formal","int",0)],None,None,None,0)
t2_print = method_record("print","Out","public","static",[variable_record("f","formal","float",0)],None,None,None,0)
t3_print = method_record("print","Out","public","static",[variable_record("b","formal","boolean",0)],None,None,None,0)
t4_print = method_record("print","Out","public","static",[variable_record("s","formal","string",0)],None,None,None,0)
Out = class_record("Out",None,None,[t1_print,t2_print,t3_print,t4_print],None,[],0)
'''
#>>>>>>>>>>>>>>>>>>>>>>data structures<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
'''
class_table = [In,Out]
method_table = [scan_int,scan_float,t1_print,t2_print,t3_print,t4_print]
'''
class_table = []
method_table = []
field_table = []
constructor_table = []


def createPrintRecurr(line):
    
    if line.__class__.__name__ == 'block_record':
        output = "Block([\n"
        first = True
        for l in line.block:
            if l == None:
                break
            if not first:
                output += ' , '
                first = False
            output += createPrintRecurr(l)
        output += "])"
        return output
    elif line.__class__.__name__ == 'if_record':
        output = "If([\n"
        output += "Condition(\n"+createPrintRecurr(line.conditional)
        output += ")\n"
        output += "Then(\n"+createPrintRecurr(line.then_block)
        output += ")\n"
        output += "Else(\n"+createPrintRecurr(line.else_block)
        output += ")\n])"
        return output
    elif line.__class__.__name__ == 'while_record':
        output += "While([\n"
        output += "Condition(\n"+createPrintRecurr(line.conditional)
        output += ")\n"
        output += createPrintRecurr(line.loop_block)
        output += "\n])"
        return output
    elif line.__class__.__name__ == 'for_record':
        output += "For([\n"
        output += "Initializer(\n"+createPrintRecurr(line.initializer)
        output += ")\n"
        output += "Condition(\n"+createPrintRecurr(line.conditional)
        output += ")\n"
        output += "UpdateExpr(\n"+createPrintRecurr(line.update_expr)
        output += ")\n"
        output += createPrintRecurr(line.loop_body)
        output += "\n])"
        return output
    elif line.__class__.__name__ == 'return_record':
        output += "Return(\n"
        output += createPrintRecurr(line.return_val)
        output += ")"
        return output
    elif line.__class__.__name__ == 'expressionStatement_record':
        output = "Expr( "
        output += createPrintRecurr(line.expression)
        output += ")"
        return output
    elif line.__class__.__name__ == 'autoExpression_record':
        return "Auto(" + createPrintRecurr(line.operand) + ", " + line.auto_type + ", " + line.tense + ")"
    elif line.__class__.__name__ == 'assignExpression_record':
        return "Assign(" + createPrintRecurr(line.assignee) + ", " + createPrintRecurr(line.assigner) + ")"
    elif line.__class__.__name__ == 'binaryExpression_record':
        return "Binary(" + line.operation +", " + createPrintRecurr(line.leftOperand) + ", " + createPrintRecurr(line.rightOperand) + ")"
    elif line.__class__.__name__ == 'fieldAccessExpression_record':
        return "Field-access(" + line.base.name + ", " + str(line.field) + ")"
    elif line.__class__.__name__ == 'const_record':
        return "Constant (" + line.type +"-constant(" + str(line.value) + ")"
    elif line.__class__.__name__ == 'newExpression_record':
        return "New-object(" + line.base + ", [" + (", ".join(createPrintRecurr(e) for e in line.args) if len(line.args) != 0 else "") + "])"
    elif line.__class__.__name__ == 'return_record':
        if (line.return_val != None):
            return "Return(" + createPrintRecurr(line.return_val) +  ")"
        else:
            return "Return( )"
    elif line.__class__.__name__ == 'methodCallExpression_record':
        return "Method-call(" + createPrintRecurr(line.base) + ", " + line.method_name + ", [" + (", ".join(createPrintRecurr(e) for e in line.args) if len(line.args) != 0 else "") + "])"
    elif line.__class__.__name__ == 'varExpression_record':
        return "Variable(" + str(line.id) + ")"
    elif line.__class__.__name__ == 'referenceExpression_record':
        return line.ref_type
    elif line.__class__.__name__ == 'list':
        return ""
    else:
        return (line.__class__.__name__)
    



#>>>>>>>>>>>>>>>>>>>>>Turn parse tree into needed classes<<<<<<<<<<<<<<<<<<<,,,
def check(file):


    data = open(file).read()



    prog = parser.parse(data, debug=False)
    if not isinstance(prog,tuple):
        prog = (prog,)
    for i in typeChecker.types.values():
        print(vars(i))
    # for item in prog:
    #     class_table.append(item)
    #print(prog)

    for classes in prog:
        class_table.append(classes)
        for constructor in classes.constructors:
            constructor_table.append(constructor)
        for methods in classes.methods:
            method_table.append(methods)
        for fields in classes.fields:
            fields.className = classes.name
            field_table.append(fields)
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
    '''
    if(prog):
        print(prog)
        for clazz in prog:
            print(">>>>>>>>>>CLASS<<<<<<<<<<<<,")
            print(vars(clazz))
            print(">>>>>>>>>>>>constructors")
            for const in clazz.constructors:
                print(vars(const))
                print("==========BODY========")
                for line in const.body.block:
                    print(type(line))
                    if line!=None:
                        print(vars(line))
                print("==========BODY========")
            print(">>>>>>>>>>>>methods")
            for method in clazz.methods:
                print(vars(method))
                print("==========BODY========")
                for line in const.body.block:
                    print(type(line))
                    if line!=None:
                        print(vars(line))
                print("==========BODY========")
            print(">>>>>>>>>>>>>fields")
            for field in clazz.fields:
                print(vars(field))
        '''


#>>>>>>>>>>>>>>>>>>>>print out of classes data structure<<<<<<<<<<<<<<<<<<
    
    if(prog):
        for clazz in class_table:
            if clazz.name == 'In' or clazz.name == 'Out':
                continue
            print("-------------------------------------------------------------------------")
            print("- Class Name: "+clazz.name)
            if(clazz.superName == None):
                print("Superclass Name:")
            else:
                print("Superclass Name: "+str(clazz.superName))
            print("Fields:")
            if(clazz.fields):
                for field in clazz.fields:
                    if(field.applicability == None):
                        if(field.visibility == None):
                            print("FIELD "+str(field.ID)+", "+str(field.name)+", "+str(field.className)+", public, instance, "+str(field.type))
                        else:
                            print("FIELD "+str(field.ID)+", "+str(field.name)+", "+str(field.className)+", "+str(field.visibility)+", instance, "+str(field.type))
                    else:
                        if(field.visibility == None):
                            print("FIELD "+str(field.ID)+", "+str(field.name)+", "+str(field.className)+", public, "+str(field.applicability)+", "+str(field.type))
                        else:
                            print("FIELD "+str(field.ID)+", "+str(field.name)+", "+str(field.className)+", "+str(field.visibility)+", "+str(field.applicability)+", "+str(field.type))
            print("Constructors:")
            if(clazz.constructors):
                for constructor in clazz.constructors:
                    if(constructor.visibility == None):
                        print("CONSTRUCTOR: "+str(constructor.ID)+", public")
                    else:
                        print("CONSTRUCTOR: "+str(constructor.ID)+", "+str(constructor.visibility))
                    if(constructor.parameters):
                        print("Constructor parameters: ",end="")
                        idx = 0
                        for param in constructor.parameters:
                            if(idx != len(constructor.parameters) - 1):
                                print(str(param.ID)+ ", ",end="")
                            else:
                                print(str(param.ID),end="")
                            idx += 1
                    else:
                        print("Constructor parameters:", end="")
                    print("\nVariable Table:")
                    if(constructor.variable_table):
                        for variable in constructor.variable_table:
                            print("VARIABLE "+str(variable.ID)+ ", "+str(variable.name)+", "+str(variable.kind)+", "+str(variable.type))
                    if(constructor.body):
                        print("Constructor Body:\n" + createPrintRecurr(constructor.body)) #NEEDS TO BE FIXED
                    else:
                        print("Constructor Body:")
            print("Methods:")
            if(clazz.methods):
                for method in clazz.methods:
                    if(method.visibility == None):
                        if(method.applicability == None):
                            print("METHOD: "+str(method.ID)+", "+method.name+", "+method.className+", public, instance, "+str(method.returnType))
                        else:
                            print("METHOD: "+str(method.ID)+", "+method.name+", "+method.className+", public, "+str(method.applicability)+", "+str(method.returnType))
                    else:
                        if(method.applicability == None):
                            print("METHOD: "+str(method.ID)+", "+method.name+", "+method.className+", "+str(method.visibility)+", instance, "+str(method.returnType))
                        else:
                            print("METHOD: "+str(method.ID)+", "+method.name+", "+method.className+", "+str(method.visibility)+", "+str(method.applicability)+", "+str(method.returnType))
                    if(method.parameters):
                        print("Method parameters: ",end="")
                        idx = 0
                        for param in method.parameters:
                            if(idx != len(method.parameters) - 1):
                                print(str(param.ID)+ ", ",end="")
                            else:
                                print(str(param.ID),end="")
                            idx += 1
                    else:
                        print("Method parameters:", end="")
                    print("\nVariable Table:")
                    if(method.variable_table):
                        for variable in method.variable_table:
                            print("VARIABLE "+str(variable.ID)+ ", "+str(variable.name)+", "+str(variable.kind)+", "+str(variable.type))
                    if(method.body):
                        print("Method Body:\n" + createPrintRecurr(method.body)) #NEEDS TO BE FIXE
                        
                    else:
                        print("Method Body:")


if __name__ == "__main__":
    sys.argv.append("OurCompiler/hw2_testing_subset/26.decaf")
    if( len(sys.argv)<2):
        print("Too few args")
        sys.exit(1)
    check(sys.argv[1])
    sys.exit(0)






