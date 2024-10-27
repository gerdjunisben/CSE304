# Benjamin Gerdjunis 
# SB ID: 115962358
# Net ID: bgerdjunis
# Donato Zampini
# SB ID: 114849209
# Net ID: dzampini

import ply.yacc as yacc
from decaf_lexer import tokens
from decaf_lexer import newline_count

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
    if len(p) == 8:
        p[0] = {'structure_type':'class','Class name':p[2], 'Super class name':p[4], 'body':p[6]}
    else:
        p[0] = {'structure_type':'class','Class name':p[2], 'Super class name':None,'body':p[4]}

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
    p[0] = {'structure_type':'field','Visibility/Applicability':p[1],'Declaration':p[2]}
        
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
    p[0] = {'structure_type':'Variable Declaration' ,'Type':p[1], 'Variable Names':p[2]}

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
    p[0] = p[1]


def p_method_decl(p):
    '''method_decl : modifier type ID LPAREN RPAREN block            
                    | modifier VOID ID LPAREN RPAREN block
                    | modifier type ID LPAREN formals RPAREN block   
                    | modifier VOID ID LPAREN formals RPAREN block'''     
    if p[2] == 'void':
        if len(p) == 7:
            p[0] = {'structure_type':'method','Visibility/Applicability': p[1], 'Method name': p[3], 'Body': p[6]}
        else:
            p[0] = {'structure_type':'method','Visibility/Applicability': p[1], 'Method name': p[3], 'Parameters': p[5], 'Body': p[7]}
    else:
        if len(p) == 7:
            p[0] = {'structure_type':'method','Visibility/Applicability': p[1], 'Return type':p[2],'Method name': p[3],   'Body': p[6]}
        else:
            p[0] = {'structure_type':'method','Visibility/Applicability': p[1], 'Return type':p[2],'Method name': p[3], 'Parameters': p[5],  'Body': p[7]}



def p_constructor_decl(p):
    '''constructor_decl : modifier ID LPAREN RPAREN block
                        | modifier ID LPAREN formals RPAREN block'''
    if len(p) ==7:
        p[0] = {'structure_type':'constructor','Visibility':p[1],  'Class name':p[2], 'Parameters':p[4],'body':p[6]}
    else:
        p[0] = {'structure_type':'constructor','Visibility':p[1], 'Class name':p[2], 'Parameters':None, 'body':p[5]}


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
    p[0] = {'type':p[1], 'variable':p[2]}


def p_block(p):
    '''block : LBRACE block_end RBRACE'''
    p[0] = p[2]

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
            p[0] = {'structure_type':'if', 'Conditional':p[3],'Then body':p[5]}
        else:
            p[0] = {'structure_type':'if', 'Conditional':p[3],'Then body':p[5], 'Else body':p[7]}
    elif p[1] == 'while':
        p[0] = {'structure_type':'while', 'Conditional':p[3], 'While body':p[5]}
    elif p[1] == 'for':
        p[0] = {'structure_type':'for','Initialize': p[3], 'Conditional': p[5], 'Increment': p[7], 'For body': p[9]}
    elif p[1] =='return':
        if len(p) ==4:
            p[0]={'structure_type':'return','Return value':p[2]}
        else:
            p[0] = {'structure_type':'return'}
    elif len(p) == 3 and p[2] == ';':
        if p[1] == 'break':
            p[0] = {'structure_type':'break'}
        elif p[1] =='continue':
            p[0] = {'structure_type':'continue'}
        else:
            p[0] = p[1]
    elif len(p) == 2 and p[1] != ';':
        p[0] = {'structure_type':'block','body':p[1]}

def p_literal(p):
    '''literal : INTCONST
                | FLOATCONST
                | STRINGCONST
                | NULL
                | TRUE
                | FALSE'''
    if isinstance(p[1],int):
        p[0] = {'structure_type':'integer constant','value':p[1]}
    elif p[1] == "true" or p[1] == "false":
        p[0] = {'structure_type':'boolean constant','value':p[1]}
    elif p[1] == "null":
        p[0] = {'structure_type':'null constant','value':p[1]};
    elif isinstance(p[1],float):
        p[0] = {'structure_type':'float constant','value':p[1]}
    else:
        p[0] = {'structure_type':'string constant','value':p[1]}


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
        p[0] = p[1]
    elif p[1] == 'new':
        if len(p) ==5:
            p[0] = {'structure_type':'new' , 'id':p[2]}
        else:
            p[0] = {'structure_type':'new', 'id':p[2],'arguments':p[4]}
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
        p[0] = {'Field name':p[1]}
    else:
        p[0] = {'Class name':p[1],'Field name':p[3]}


def p_method_invocation(p):
    '''method_invocation : field_access LPAREN RPAREN
                        | field_access LPAREN arguments RPAREN'''
    if len(p) == 4:
        p[0] = {'structure_type':'method invocation',**p[1]}
    else:
        p[0] = {'structure_type':'method invocation',**p[1], 'args':p[3]}


def p_expr(p):
    '''expr : primary
            | assign
            | expr arith_op expr
            | expr bool_op expr
            | unary_op expr'''
    if len(p) ==2:
        p[0] = p[1]
    elif len(p) ==3:
        p[0] = {'structure_type':'unary expression','operator':p[1],'expression':p[2]}
    else:
        p[0] = {'structure_type':'binary expression','operator':p[2],'first expression':p[1],'second expression':p[3]}


def p_assign(p):
    '''assign : lhs EQUALS expr
            | lhs PLUSPLUS
            | PLUSPLUS lhs
            | lhs MINUSMINUS
            | MINUSMINUS lhs'''
    if p[2] == '=':
        p[0] = {'structure_type':'assignment','assignment':(p[1],'=',p[3])}
    else:
        p[0] = {'structure_type':'auto expression','assignment':(p[1],p[2])}

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
    p[0] = p[1]


def p_error(p):
    if not p:
        print("SYNTAX error due to EOF (possibly an incomplete body)")
    else:
        print(f"SYNTAX error from '{p.value}' at line {newline_count}")

bparser = yacc.yacc(start = "program")



def parse(data, debug=False):
    bparser.error = 0
    p = bparser.parse(data, debug=debug)
    if bparser.error:
        return None
    return p