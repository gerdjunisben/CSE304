# Benjamin Gerdjunis 
# SB ID: 115962358
# Net ID: bgerdjunis
# Donato Zampini
# SB ID: 114849209
# Net ID: dzampini

import decaf_lexer as lexer
import decaf_parser as parser
import os
import re



for file in os.listdir('HW3/hw2_testing_subset'):
    #if(re.search("20",file)):
        f = os.path.join('HW3/hw2_testing_subset',file)




        data = open(f).read()


        prog = parser.parse(data, debug=False)
        if(prog):
            print(f, "success")
        else:
            print(f, "fail")

        #print(prog)