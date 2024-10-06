import ply.yacc as yacc
from decaf_lexer import tokens

def p_empty(p):
    '''empty :'''
    pass

def p_program(p):
    '''program : class_decl
                | class_decl program
                | empty'''
    if len(p) ==2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] +[p[2]]

def p_class_decl(p):
    '''class_decl : CLASS ID EXTENDS ID LBRACE class_body_decl RBRACE
                  | CLASS ID LBRACE class_body_decl RBRACE'''
    if len(p) == 7:
        p[0] = {'id':p[2], 'super_id':p[4], 'class_body_decl':p[6]}
    else:
        p[0] = {'id':p[2], 'class_body_decl':p[4]}

def p_class_body_decl(p):
    '''class_body_decl : field_decl
                    | method_decl
                    | constructor_decl
                    | field_decl class_body_more
                    | method_decl class_body_more
                    | constructor_decl class_body_more'''
    if len(p) == 2:
        p[0] = [p[1]]  
    else:
        p[0] = p[1] + [p[2]]


def p_class_body_more(p):
    '''class_body_more : empty
                    | field_decl class_body_more
                    | method_decl class_body_more
                    | constructor_decl class_body_more'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + [p[2]]


def p_field_decl(p):
    '''field_decl : modifier var_decl'''
    p[0] = {'modifier':p[1],'var_decl':p[2]}
        
def p_modifier(p):
    '''modifier : PUBLIC STATIC
                | PRIVATE STATIC
                | PUBLIC
                | PRIVATE
                | STATIC
                | empty'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    elif len(p) ==2:
        p[0] = p[1]
    else:
        p[0] = None
    
def p_var_decl(p):
    '''var_decl : type variables'''
    p[0] = {'type':p[1], 'variables':p[2]}

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
        p[0] = [p[1]] + p[3]
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
    if len(p) >4:
        p[0] = {'modifier':p[1], 'type':p[2], 'id':p[3], 'formals':p[5],'block':p[6]}
    else:
        p[0] = {'modifier':p[1], 'type':p[2], 'id':p[3], 'block':p[5]}


def p_constructor_decl(p):
    '''constructor_decl : modifier ID LPAREN RPAREN block
                        | modifier ID LPAREN formals RPAREN block'''
    if len(p) >4:
        p[0] = {'modifier':p[1],  'id':p[2], 'formals':p[4],'block':p[6]}
    else:
        p[0] = {'modifier':p[1], 'id':p[2], 'block':p[5]}


def p_formals(p):
    '''formals : formals COMMA formal_param 
                | formal_param
                | empty'''
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = [p[1]] + p[2]


def p_formal_param(p):
    '''formal_param : type variable'''
    p[0] = {'type':p[1], 'variable':p[2]}


def p_block(p):
    '''block : LBRACE stmt RBRACE'''
    p[0] = p[2]


def p_stmt(p):
    '''stmt : IF LPAREN expr RPAREN stmt
            | IF LPAREN expr RPAREN stmt ELSE stmt
            | WHILE LPAREN expr RPAREN stmt
            | FOR LPAREN stmt_expr SEMICOLON expr SEMICOLON stmt_expr RPAREN stmt
            | FOR LPAREN SEMICOLON expr SEMICOLON stmt_expr RPAREN stmt
            | FOR LPAREN stmt_expr SEMICOLON  SEMICOLON stmt_expr RPAREN stmt
            | FOR LPAREN stmt_expr SEMICOLON expr SEMICOLON  RPAREN stmt
            | FOR LPAREN  SEMICOLON  SEMICOLON stmt_expr RPAREN stmt
            | FOR LPAREN stmt_expr SEMICOLON  SEMICOLON RPAREN stmt
            | FOR LPAREN  SEMICOLON expr SEMICOLON RPAREN stmt
            | FOR LPAREN  SEMICOLON  SEMICOLON  RPAREN stmt
            | RETURN SEMICOLON
            | RETURN expr SEMICOLON
            | stmt_expr SEMICOLON
            | BREAK SEMICOLON
            | CONTINUE SEMICOLON
            | block
            | var_decl
            | SEMICOLON'''
    
    if p[1] == 'if':
        if len(p) == 6:
            p[0] = {'expr':p[3],'stmt':p[5]}
        else:
            p[0] = {'expr':p[3],'stmt':p[5], 'stmt':p[7]}
    elif p[1] == 'while':
        p[0] = {'expr':p[3], 'stmt':p[5]}
    elif p[1] == 'for':
        if p[3] ==';':
            if p[4]==';':
                if p[5]==')':
                    p[0] = {'stmt':p[6]}
                else:
                    p[0] = {'stmt_expr':p[5], 'stmt':p[7]}
            else:
                if p[6]==')':
                    p[0] = {'expr':p[4], 'stmt':p[7]}
                else:
                    p[0] = {'expr':p[4],'expr':p[6], 'stmt':p[8]}
        else:
            if p[5]==';':
                if p[6]==')':
                    p[0] = {'stmt_expr':p[3], 'stmt':p[7]}
                else:
                    p[0] = {'stmt_expr':p[3], 'stmt_expr':p[5], 'stmt':p[8]}
            else:
                if p[7]==')':
                    p[0] = {'stmt_expr':p[3],'expr':p[5], 'stmt':p[8]}
                else:
                    p[0] = {'stmt_expr':p[3],'expr':p[5],'stmt_expr':p[7], 'stmt':p[9]}
    elif p[1] =='return':
        if len(p) ==3:
            p[0]=p[2];
    elif (p[1] == 'break' or p[1]== 'continue' or p[1] ==';'):
        p[0] = None
    else:
        p[0] = p[1]

def p_literal(p):
    '''literal : INTCONST
                | FLOATCONST
                | STRINGCONST
                | NULL
                | TRUE
                | FALSE'''
    if p[1] =='null' or p[1] =='true' or p[1]=='false':
        p[0] = None
    else:
        p[0] = p[1];


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
        p[0] = None
    elif p[1] == 'new':
        if len(p) == 5:
            p[0] = {'id':p[2]}
        else:
            p[0] = {'id':p[2],'arguments':p[4]}
    elif p[1] =='(':
        p[0] = p[2]
    else:
        p[0] = p[1]
            
def p_arguments(p):
    '''arguments : expr
                | arguments COMMA expr
                | empty'''
    if len(p) == 1:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]

def p_lhs(p):
    '''lhs : field_access'''
    p[0] = p[1]


def p_field_access(p):
    '''field_access : primary PERIOD ID
                    | ID'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]


def p_method_invocation(p):
    '''method_invocation : field_access LPAREN RPAREN
                        | field_access LPAREN arguments RPAREN'''
    if len(p) ==4:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]


def p_expr(p):
    '''expr : primary
            | assign
            | expr arith_op expr
            | expr bool_op expr
            | unary_op expr'''
    if len(p) ==2:
        p[0] = p[1]
    elif len(p) ==3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1] + p[2] + p[3]


def p_assign(p):
    '''assign : lhs EQUALS expr
            | lhs PLUSPLUS
            | PLUSPLUS lhs
            | lhs MINUSMINUS
            | MINUSMINUS lhs'''
    if p[2] == '=':
        p[0] = p[1] + p[3]
    elif(p[1] == '++' or p[1] =='--'):
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_arith_op(p):
    '''arith_op : PLUS
                | MINUS
                | TIMES
                | DIVIDE'''
    p[0] = None

def p_bool_op(p):
    '''bool_op : AND
                | OR
                | EQUALSCOMPARE
                | NOTEQUALS
                | LESSTHAN
                | GREATERTHAN
                | LESSTHANOREQ
                | GREATERTHANOREQ'''
    p[0] = None

def p_unary_op(p):
    '''unary_op : PLUS
                | MINUS
                | NOT'''
    p[0] = None

def p_stmt_expr(p):
    '''stmt_expr : assign
                | method_invocation'''


parser = yacc.yacc(start = "program")
