# Benjamin Gerdjunis 
# SB ID: 115962358
# Net ID: bgerdjunis
# Donato Zampini
# SB ID: 114849209
# Net ID: dzampini

import decaf_lexer as lexer
import decaf_parser as parser
import sys


def check(file):


    data = open(file).read()



    prog = parser.parse(data, debug=False)
    if(prog):
        print("Yes")
        print(prog)
        return 1
    return 0



if __name__ == "__main__":
    if( len(sys.argv)<2):
        print("Too few args")
        sys.exit(1)
    check(sys.argv[1])
    sys.exit(0)