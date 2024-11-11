# Benjamin Gerdjunis 
# SB ID: 115962358
# Net ID: bgerdjunis
# Donato Zampini
# SB ID: 114849209
# Net ID: dzampini

import ply.yacc as yacc
from decaf_lexer import tokens
from decaf_lexer import global_symbol_table

from decaf_ast import constructor_record
from decaf_ast import class_record
from decaf_ast import method_record
from decaf_ast import field_record

from decaf_ast import variable_record

from decaf_ast import statement_record
from decaf_ast import if_record
from decaf_ast import while_record
from decaf_ast import for_record
from decaf_ast import return_record
from decaf_ast import expressionStatement_record
from decaf_ast import block_record
from decaf_ast import controlFlow_record

from decaf_ast import expression_record
from decaf_ast import const_record
from decaf_ast import varExpression_record
from decaf_ast import unaryExpression_record
from decaf_ast import binaryExpression_record
from decaf_ast import assignExpression_record
from decaf_ast import autoExpression_record
from decaf_ast import fieldAccessExpression_record
from decaf_ast import methodCallExpression_record
from decaf_ast import newExpression_record
from decaf_ast import referenceExpression_record





precedence = (
    ('left','EQUALS'),
    ('left','OR'),
    ('left','AND'),
    ('left','EQUALSCOMPARE','NOTEQUALS'),
    ('left', 'LESSTHAN','GREATERTHAN','LESSTHANOREQ','GREATERTHANOREQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right','MINUS','NOT'),
)



def p_empty(p):
    '''empty :'''
    pass


def p_program(p):
    '''program : class_decl
                | class_decl program'''
    if len(p) ==2:
        p[0] = p[1]
    else:
        p[0] = (p[1],p[2])

def p_class_decl(p):
    '''class_decl : CLASS ID EXTENDS ID LBRACE class_body_decl RBRACE
                  | CLASS ID LBRACE class_body_decl RBRACE'''
    global latest_class

    constructors = []
    methods = []
    fields =[]
    if len(p) == 8:
        
        for thing in p[6]:
            if isinstance(thing,constructor_record):
                constructors = constructors + [thing]
            elif isinstance(thing,method_record):
                thing.className = p[2]
                methods = methods + [thing]
            elif isinstance(thing,list)  and isinstance(thing[0],field_record):
                fields = fields + thing
        p[0] = class_record(p[2],p[4],constructors,methods,fields,p[6],p.lineno(1))
    else:
        for thing in p[4]:
            if isinstance(thing,constructor_record):
                constructors = constructors + [thing]
            elif isinstance(thing,method_record):
                thing.className = p[2]
                methods = methods + [thing]
            elif isinstance(thing,list)  and isinstance(thing[0],field_record):
                fields = fields + thing
        p[0] = class_record(p[2],None,constructors,methods,fields,p[4],p.lineno(1))
        
def p_class_body_decl(p):
    '''class_body_decl : class_body_sub_decls'''
    p[0] = p[1]

def p_class_body_sub_decls(p):
    '''class_body_sub_decls : field_decl SEMICOLON class_body_sub_decls
                    | method_decl class_body_sub_decls
                    | constructor_decl class_body_sub_decls
                    | field_decl SEMICOLON
                    | constructor_decl
                    | method_decl
                    | empty'''
    if len(p) == 2 or (len(p)==3 and p[2]==';'):
        p[0] = [p[1]]
    elif (len(p) == 3):
        p[0] = [p[1]] +  p[2]
    else:
        p[0] = [p[1]] + p[3]



def p_field_decl(p):
    '''field_decl : modifier var_decl'''
    app = None
    vis = None

    if(p[1] != None and p[1]['Visibility'] != None):
        vis = p[1]['Visibility']
    elif(p[1] != None and p[1]['Applicability'] != None):
        app = p[1]['Applicability']

    fields = []
    for var in p[2]:
        fields = fields + [field_record(var.name,None,vis,app,var.type,var.line)]
    p[0] = fields
    
def p_modifier(p):
    '''modifier : visibility applicability
                | visibility
                | applicability
                | empty'''
    if len(p) ==2:
        p[0] = p[1]
    else:
        p[0] ={**p[1], **p[2]}


def p_visibility(p):
    '''visibility : PUBLIC
                  | PRIVATE'''
    p[0] = {'Visibility':p[1]}

def p_applicability(p):
    '''applicability : STATIC'''
    p[0] = {'Applicability':p[1]}
    
def p_var_decl(p):  
    '''var_decl : type variables'''
    names = p[2]
    if(isinstance(names,tuple)):
        p[0] = [variable_record(names[0],None,p[1],names[1])]
    else:
        vars = []
        for name in names:
            vars = vars + [variable_record(name[0],None,p[1],name[1])]
        p[0] = vars
    
def p_type(p):
    '''type : INT
            | FLOAT
            | BOOLEAN
            | VOID
            | ID'''
    if p[1] == 'void':
        p[0] = None
    else:
        p[0] = p[1];


def p_variables(p):
    '''variables : variable
                | variables COMMA variable
                | empty'''
    if len(p)==2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = [p[1]] + [p[3]]
    else:
        p[0] = []

def p_variable(p):
    '''variable : ID'''
    p[0] = (p[1],p.lineno(1))


def p_method_decl(p):
    '''method_decl : modifier type ID LPAREN RPAREN block            
                    | modifier VOID ID LPAREN RPAREN block
                    | modifier type ID LPAREN formals RPAREN block   
                    | modifier VOID ID LPAREN formals RPAREN block'''    

    vis = None
    app = None
    if(p[1] != None and p[1]['Visibility'] != None):
        vis = p[1]['Visibility']
    elif(p[1] != None and p[1]['Applicability'] != None):
        app = p[1]['Applicability']
    var_tab = []
    if p[2] == 'void':
        if len(p) == 7:
            p[0] = method_record(p[3],None,vis,app,[],'void',var_tab,p[6],p.lineno(3))
        else:
            p[0] = method_record(p[3],None,vis,app,p[5],'void',var_tab,p[7],p.lineno(3))
    else:
        if len(p) == 7:
            p[0] = method_record(p[3],None,vis,app,[],p[2],var_tab,p[6],p.lineno(3))
        else:
            p[0] = method_record(p[3],None,vis,app,p[5],p[2],var_tab,p[7],p.lineno(3))



def p_constructor_decl(p):
    '''constructor_decl : modifier ID LPAREN RPAREN block
                        | modifier ID LPAREN formals RPAREN block'''

    if len(p) ==7:

        p[0] = constructor_record(p[2],p[1],p[4],[],p[6],p.lineno(2))
    else:
        p[0] = constructor_record(p[2],p[1],[],[],p[5],p.lineno(2))


def p_formals(p):
    '''formals : formals COMMA formal_param 
                | formal_param
                | empty'''
    if len(p)==2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_formal_param(p):
    '''formal_param : type variable'''
    p[0] = variable_record(p[2][0],'formal',p[1],p.lineno(1))


def p_block(p):
    '''block : LBRACE block_end RBRACE'''
    var_tab = []
    p[0] = block_record(p[2],var_tab,p.lineno(1))


def p_block_end(p):
    '''block_end : stmt
                | stmt block_end
                | empty'''
    if(len(p) == 3):
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]


def p_stmt(p):
    '''stmt : IF LPAREN expr RPAREN stmt
            | IF LPAREN expr RPAREN stmt ELSE stmt
            | WHILE LPAREN expr RPAREN stmt
            | FOR LPAREN stmt_expr SEMICOLON expr SEMICOLON stmt_expr RPAREN stmt
            | RETURN SEMICOLON
            | RETURN expr SEMICOLON
            | stmt_expr SEMICOLON
            | BREAK SEMICOLON
            | CONTINUE SEMICOLON
            | block
            | var_decl SEMICOLON
            | SEMICOLON'''
    
    if p[1] == 'if':
        if len(p) == 6:
            p[0] = if_record(p[3],p[5],[],p.lineno(1))
        else:
            p[0] = if_record(p[3],p[5],p[7],p.lineno(1))
    elif p[1] == 'while':
        p[0] = while_record(p[3],p[5],p.lineno(1))
        
    elif p[1] == 'for':
        p[0] = for_record(p[3],p[5],p[7],p[9],p.lineno(1))
    elif p[1] =='return':
        if len(p) ==4:
            p[0]=return_record(p[2],p.lineno(1))
        else:
            p[0] = return_record(None,p.lineno(1))
    elif len(p) == 3 and p[2] == ';':
        if p[1] == 'break':
            p[0] = controlFlow_record('break',p.lineno(1))
        elif p[1] =='continue':
            p[0] = controlFlow_record('continue',p.lineno(1))
        else:
            p[0] = p[1]
    elif len(p) == 2 and p[1] != ';':
        p[0] = block_record(p[1],[],p.lineno(1))

def p_literal(p):
    '''literal : INTCONST
                | FLOATCONST
                | STRINGCONST
                | NULL
                | TRUE
                | FALSE'''
    if isinstance(p[1],int):
        p[0] = const_record('int',p[1],p.lineno(1))
    elif p[1] == "true" or p[1] == "false":
        p[0] = const_record('bool',p[1],p.lineno(1))
    elif p[1] == "null":
        p[0] = const_record('null',p[1],p.lineno(1))
    elif isinstance(p[1],float):
        p[0] = const_record('float',p[1],p.lineno(1))
    else:
        p[0] = const_record('string',p[1],p.lineno(1))


def p_primary(p):
    '''primary : literal
            | THIS
            | SUPER
            | LPAREN expr RPAREN
            | NEW ID LPAREN arguments RPAREN
            | NEW ID LPAREN RPAREN
            | lhs
            | method_invocation'''
    if p[1] == 'this' or p[1]=='super':
        p[0] = referenceExpression_record(p[1],p.lineno(1))
    elif p[1] == 'new':
        if len(p) ==5:
            p[0] = newExpression_record(p[2],[],p.lineno(1))
        else:
            p[0] = newExpression_record(p[2],p[4],p.lineno(1))
    elif p[1] =='(':
        p[0] = p[2]
    else:
        p[0] = p[1]
            
def p_arguments(p):
    '''arguments : expr
                | arguments COMMA expr
                | empty'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_lhs(p):
    '''lhs : field_access'''
    p[0] = p[1]


def p_field_access(p):
    '''field_access : primary PERIOD ID
                    | ID'''
    if len(p) == 2:
        p[0] = varExpression_record(p[1],p.lineno(1))
    else:
        p[0] = fieldAccessExpression_record(p[1],p[3],p.lineno(1))


def p_method_invocation(p):
    '''method_invocation : field_access LPAREN RPAREN
                        | field_access LPAREN arguments RPAREN'''
    if len(p) == 4:
        p[0] = methodCallExpression_record(p[1],[],p.lineno(1))
    else:
        p[0] = methodCallExpression_record(p[1],p[3],p.lineno(1))
    

def p_expr(p):
    '''expr : primary
            | assign
            | expr arith_op expr
            | expr bool_op expr
            | unary_op expr'''
    if len(p) ==2:
        p[0] = p[1]
    elif len(p) ==3:
        p[0] = unaryExpression_record(p[1],p[2],p.lineno(1))
    else:
        p[0] = binaryExpression_record(p[1],p[2],p[3],p.lineno(1))
        
def p_assign(p):
    '''assign : lhs EQUALS expr
            | lhs PLUSPLUS
            | PLUSPLUS lhs
            | lhs MINUSMINUS
            | MINUSMINUS lhs'''
    if p[2] == '=':
        p[0] = assignExpression_record(p[1],p[3],p.lineno(1))
    else:
        if(p[1] == '++' or p[1] =='--'):
            p[0] = autoExpression_record(p[2],p[1],'pre',p.lineno(1))
        else:
            p[0] = autoExpression_record(p[1],p[2],'post',p.lineno(1))

def p_arith_op(p):
    '''arith_op : PLUS
                | MINUS
                | TIMES
                | DIVIDE'''
    p[0] = p[1]

def p_bool_op(p):
    '''bool_op : AND
                | OR
                | EQUALSCOMPARE
                | NOTEQUALS
                | LESSTHAN
                | GREATERTHAN
                | LESSTHANOREQ
                | GREATERTHANOREQ'''
    p[0] = p[1]

def p_unary_op(p):
    '''unary_op : PLUS
                | MINUS
                | NOT'''
    p[0] = p[1]

def p_stmt_expr(p):
    '''stmt_expr : assign
                | method_invocation'''
    p[0] = expressionStatement_record(p[1],p.lineno(1)) 



def p_error(p):
    if not p:
        print("SYNTAX error due to EOF (possibly an incomplete body)")
    else:
        print(f"SYNTAX error from '{p.value}' at line {p.lineno}")

bparser = yacc.yacc(start = "program")


def parse(data, debug=False):
    bparser.error = 0
    p = bparser.parse(data, debug=debug)
    '''
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<")
    print(vars(global_symbol_table.globalTable))
    for name,scope in global_symbol_table.globalTable.minis.items():
        print(name + " : " + str(vars(scope)))
        if(len(scope.minis)>0):
            for name2,scope2 in scope.minis.items():
                print(name2 + " : " + str(vars(scope2)))
    '''
    if bparser.error:
        return None
    return p