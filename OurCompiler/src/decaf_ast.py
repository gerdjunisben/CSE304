# Benjamin Gerdjunis 
# SB ID: 115962358
# Net ID: bgerdjunis
# Donato Zampini
# SB ID: 114849209
# Net ID: dzampini


import decaf_lexer as lexer
import decaf_parser as parser
import sys


#create a class that holds a Decaf class, then make a data structure of them
#make additional classes for things like fields, methods and vars and additional data structures
#for clarity



#>>>>>>>>>>>>>>>>>>>>>> Class Table <<<<<<<<<<<<<<<<<<<<<<<<<



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


#>>>>>>>>>>>>>>>>>>>>>> Variable Table <<<<<<<<<<<<<<<<<<<

class variable_record:
    varID = 0
    def __init__(self,name,kind,type):
        self.name = name
        self.kind = kind  #local or formal <3
        self.type = type
        self.ID = variable_record.varID
        variable_record.varID +=1


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
    if(prog):
        print(prog)
        for clazz in prog:
            print(clazz.name)
            print("constructors")
            for const in clazz.constructors:
                print(const.parameters)
        '''
        for clazz in prog:
            constructors = None
            methods = None
            fields = None
            for thing in clazz['body']:   #############Probably start adding here
                if thing == None:
                    pass
                elif thing['structure_type'] == 'method':
                    pass
                elif thing['structure_type'] == 'constructor':
                    pass
                else:
                    pass
            newClass = class_record(clazz['Class name'],clazz['Super class name'],constructors,methods,fields)
            class_table.append(newClass)



        ###Print to see it worked
        for i in class_table:
            print(i.name)
        '''
        return 1
    return 0



if __name__ == "__main__":
    if( len(sys.argv)<2):
        print("Too few args")
        sys.exit(1)
    check(sys.argv[1])
    sys.exit(0)





#>>>>>>>>>>>>>>>>>>>>print out of classes data structure<<<<<<<<<<<<<<<<<<

