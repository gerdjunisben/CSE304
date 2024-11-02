# Benjamin Gerdjunis 
# SB ID: 115962358
# Net ID: bgerdjunis
# Donato Zampini
# SB ID: 114849209
# Net ID: dzampini

import ply.lex as lex

from decaf_scoper import SymbolTable

global_symbol_table = SymbolTable()


# List of token names
tokens = [
    'NUMBER',
    'STRING',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'OR',
    'AND',
    'NOT',
    'EQUALS',
    'EQUALSCOMPARE',
    'NOTEQUALS',
    'LESSTHAN',
    'GREATERTHAN',
    'LESSTHANOREQ',
    'GREATERTHANOREQ',
    'DECLARE',
    'TERMINALS',
    'SYMBOLS',
    'LPAREN',
    'LBRACKET',
    'LBRACE',
    'RPAREN',
    'RBRACKET',
    'RBRACE',
    'COMMA',
    'SEMICOLON',
    'PERIOD',
    'PLUSPLUS',
    'MINUSMINUS',
    'FLOATCONST',
    'STRINGCONST',
    'INTCONST',
    'ID',
]

reserved = {
    'boolean':'BOOLEAN',
    'break':'BREAK',
    'continue':'CONTINUE',
    'class':'CLASS',
    'do':'DO',
    'else':'ELSE',
    'extends':'EXTENDS',
    'false':'FALSE',
    'float':'FLOAT',
    'for':'FOR',
    'if':'IF',
    'int':'INT',
    'new':'NEW',
    'null':'NULL',
    'private':'PRIVATE',
    'public':'PUBLIC',
    'return':'RETURN',
    'static':'STATIC',
    'super':'SUPER',
    'this':'THIS',
    'true':'TRUE',
    'void':'VOID',
    'while':'WHILE'
}

tokens = tokens + list(reserved.values())

# Regex rules
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_OR        = r'\|\|'
t_AND       = r'&&'
t_NOT       = r'!'
t_EQUALS    = r'='
t_EQUALSCOMPARE = r'=='
t_NOTEQUALS = r'!='
t_LESSTHAN  = r'<'
t_GREATERTHAN = r'>'
t_LESSTHANOREQ = r'<='
t_GREATERTHANOREQ = r'>='
t_DECLARE   = r'::='
t_TERMINALS = r'[A-Z]'
t_SYMBOLS   = r'[a-z]'
t_LPAREN    = r'\('
t_LBRACKET  = r'\['
t_RPAREN    = r'\)'
t_RBRACKET  = r'\]'
t_COMMA     = r','
t_SEMICOLON = r';'
t_PERIOD    = r'.'
t_PLUSPLUS  = r'\+\+'
t_MINUSMINUS = r'--'
t_BOOLEAN   = r'boolean' 
t_BREAK     = r'break' 
t_CONTINUE  = r'continue' 
t_CLASS     = r'class'
t_DO        = r'do'
t_ELSE      = r'else'
t_EXTENDS   = r'extends'
t_FLOAT     = r'float'
t_FOR       = r'for'
t_IF        = r'if'
t_INT       = r'int'
t_NEW       = r'new'
t_NULL      = r'null'
t_PRIVATE   = r'private'
t_PUBLIC    = r'public'
t_RETURN    = r'return'
t_STATIC    = r'static'
t_SUPER     = r'super'
t_THIS      = r'this'
t_VOID      = r'void'
t_WHILE     = r'while'


def t_LBRACE(t):
    r'\{'
    global_symbol_table.enterNewScope()
    return t

def t_RBRACE(t):
    r'\}'
    global_symbol_table.exitScope()
    return t

# Function for ID regex
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    else:
        global_symbol_table.add({'name':t.value,'id':0})
    return t

# Function for FLOATCONST regex
def t_FLOATCONST(t):
    r'(-)?\d+(\.)?\d+'
    t.value = float(t.value)
    return t

# Function for INTCONST regex
def t_INTCONST(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Function for STRINGCONST regex
def t_STRINGCONST(t):
    r'\".*\"'
    t.value = str(t.value)
    return t

# Function for NUMBER regex
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Function for STRING regex
def t_STRING(t):
    r'\".*\"'
    return str(t)


def t_newline(t):
    r'\n+'
    t.lexer.lineno+=len(t.value)


# Function for lexer to interpret and ignore comments
def t_comment(t):
    r'(//(.)*\n) | (/\*(.|\n)*?\*/)'
    t.lexer.lineno += t.value.count('\n')




# FUNCTIONS FROM PLY RECITATION LECTURE

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'



# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# END OF FUNCTIONS FROM PLY RECITATION LECTURE

# Old functions that were commented out for being bad and not working
# Tokenizes a line that contains the operator "::="
# def tokenizeTerminalLine(String:str):
#     newToken = String.split(' ').pop(0)
#     if newToken not in tokens:
#         tokens.append(newToken)

# Reads through entire program, passed as one long string
# def lexProgram(String:str):
#     lines:list[str] = str.split("\n")
#     for line in lines:
#         if "::=" in line:
#             tokenizeTerminalLine(line)

# Create lexer
lex.lex()