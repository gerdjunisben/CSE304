import ply.lex as lex

# List of token names
tokens = (
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
    'RBRACE'
)

# Regex rules
t_PLUS = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_OR = r'\|\|'
t_AND = r'&&'
t_NOT = r'!'
t_EQUALS = r'='
t_EQUALSCOMPARE = r'=='
t_NOTEQUALS = r'!='
t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'
t_LESSTHANOREQ = r'<='
t_GREATERTHANOREQ = r'>='
t_DECLARE = r'::='
t_TERMINALS = r'[A-Z]'
t_SYMBOLS = r'[a-z]'
t_LPAREN  = r'\('
t_LBRACKET = r'\['
t_LBRACE = r'\{'
t_RPAREN  = r'\)'
t_RBRACKET = r'\]'
t_RBRACE = r'\}'


#######Things I think I need tokens for ',', ';', '.', '++', '--', '&&', '||'


# Funtion for number regex
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Function for string regex
def t_STRING(t):
    r'\"\w+\"'
    return str(t)

######Make sure to set up the tokens array and the regex rules, what you wrote might not like things
######such as number. See the example in the PLY thing also brackets and junk are tokens in this language

# FUNCTIONS FROM PLY RECITATION LECTURE
# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# END OF FUNCTIONS FROM PLY RECITATION LECTURE

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

lexer = lex.lex()
data = '''
A ::=a||aB
B ::= b||ab
number = 3 + 3 + -9'''


# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)