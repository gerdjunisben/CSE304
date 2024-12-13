# Benjamin Gerdjunis 
# SB ID: 115962358
# Net ID: bgerdjunis
# Donato Zampini
# SB ID: 114849209
# Net ID: dzampini

import decaf_codegen as Compiler
import sys



if __name__ == "__main__":
    if( len(sys.argv)<2):
        print("Too few args")
        sys.exit(1)
    res = Compiler.compile(sys.argv[1])
    if(res):
        output_file = sys.argv[1][:-6] + '.ami'
        with open(output_file, 'w') as f:
            f.write(res)
    sys.exit(0)