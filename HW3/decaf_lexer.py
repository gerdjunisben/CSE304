import ply.lex as lex

reserved_words = ["boolean", "break", "continue", "class", "do", "else"
"extends", "false", "float", "for", "if", "int"
"new", "null", "private", "public", "return", "static"
"super", "this", "true", "void", "while"]

tokens:list[str] = []

# Tokenizes a line that contains the operator "::="
def createToken(String:str):
    newToken = String.split(":").pop(0)
    if newToken not in tokens:
        tokens.append(newToken)

# Reads through entire program, passed as one long string
def lexProgram(String:str):
    lines:list[str] = str.split("\n")
    for line in lines:
        if "::=" in line:
            createToken(line)

lexer = lex.lex

# # Test it out
# data = '''
# 3 + 4 * 10
#   + -20 *2
# '''

# # Give the lexer some input
# lexer.input(data)

# # Tokenize
# while True:
#     tok = lexer.token()
#     if not tok: 
#         break      # No more input
#     print(tok)