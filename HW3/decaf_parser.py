import ply.yacc as yacc

def p_empty(p):
    pass

def p_progam(p):
    '''program:class_decl
                | class_decl program'''
    if len(p) ==2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] +[p[2]]

def p_class_decl(p):
    '''class_decl:class id (extends id)? { class_body_decl }'''
    if p[3] == 'extends':
        p[0] = {'id':p[2], 'super_id':p[4], 'class_body_decl':p[6]}
    else:
        p[0] = {'id':p[2], 'class_body_decl':p[4]}

def p_class_body_decl(p):
    '''class_body_decl:field_decl
                    |method_decl
                    |constructor_decl
                    |class_body_decl field_decl
                    |class_body_decl method_decl
                    |class_body_decl constructor_decl'''
    if len(p) == 2:
        p[0] = [p[1]]  
    else:
        p[0] = [p[1]] + p[2]

def p_field_decl(p):
    '''field_decl:modifier var_decl'''
    p[0] = {'modifier':p[1],'var_decl':p[2]}
        
def p_modifier(p):
    '''modifier : (public|private)? (static)?'''
    if len(p) == 2:
        p[0] = p[1] + p[2]
    elif len(p) ==1:
        p[0] = p[1]
    else:
        p[0] = None
    
def p_var_decl(p):
    '''var_decl: type variables'''
    p[0] = {'type':p[1], 'variables':p[2]}

def p_type(p):
    '''type: int
            |float
            |boolean
            |void
            |id'''
    if p[1] == 'void':
        p[0] = None
    else:
        p[0] = p[1];


def p_variables(p):
    '''variables : variable
                | variables, variable'''
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = [p[1]] + p[2]

def p_variable(p):
    '''variable:id'''
    p[0] = p[1]


def p_method_decl(p):
    '''method_decl: modifier (type | void) id ( formals? ) block'''
    if len(p) >4:
        p[0] = {'modifier':p[1], 'type':p[2], 'id':p[3], 'formals':p[4],'block':p[5]}
    else:
        p[0] = {'modifier':p[1], 'type':p[2], 'id':p[3], 'formals':None,'block':p[5]}


def p_constructor_decl(p):
    '''constructor_decl: modifier id ( formals? ) block'''
    if len(p) >4:
        p[0] = {'modifier':p[1],  'id':p[2], 'formals':p[3],'block':p[4]}
    else:
        p[0] = {'modifier':p[1], 'id':p[2], 'formals':None,'block':p[4]}


def p_formals(p):
    '''formals: formals, formal_param 
                |formal_param'''
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = [p[1]] + p[2]


def p_formal_param(p):
    '''formal_param: type variable'''
    p[0] = p[1] + p[2]


def p_block(p):
    '''block: { stmt }'''
    p[0] = p[1]


def p_stmt(p):
    '''stmt : if ( expr ) stmt
            |if ( expr ) stmt else stmt
            |while ( expr ) stmt
            |for ( stmt_expr ; expr ; stmt_expr )stmt
            |for ( ; expr ; stmt_expr )stmt
            |for ( stmt_expr ;  ; stmt_expr )stmt
            |for ( stmt_expr ; expr ;  )stmt
            |for (  ;  ; stmt_expr )stmt
            |for ( stmt_expr ;  ; )stmt
            |for (  ; expr ; )stmt
            |for (  ;  ;  )stmt
            |return ;
            |return expr ;
            |stmt_expr;
            |break;
            |continue;
            |block
            |var_decl
            |;'''
    
    if p[1] == 'if':
        if len(p) == 6:
            p[0] = {'expr':p[3],'stmt':p[5]}
        else:
            p[0] = {'expr':p[3],'stmt':p[5], 'stmt':p[7]}
    elif p[1] == 'while':
        p[0] = {'expr':p[3], 'stmt':p[5]}
    #elif p[1] == 'for':

    elif p[1] =='return':
        if len(p) ==3:
            p[0]=p[2];
    elif (p[1] == 'break' or p[1]== 'continue' or p[1] ==';'):
        p[0] = None
    else:
        p[0] = p[1]

