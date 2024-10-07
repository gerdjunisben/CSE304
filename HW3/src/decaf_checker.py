# Benjamin Gerdjunis 
# SB ID: 115962358
# Net ID: bgerdjunis
# Donato Zampini
# SB ID: 114849209
# Net ID: dzampini

import decaf_lexer as lexer
import decaf_parser as parser


data = open('HW3/hw2_testing_subset/err3.decaf').read()


prog = parser.parse(data);
print(prog)