# Benjamin Gerdjunis 
# SB ID:
# Net ID:
# Donato Zampini
# SB ID: 114849209
# Net ID: dzampini

import decaf_lexer as lexer
import decaf_parser as parser


data = open('HW3/hw2_testing_subset/7.decaf').read()


prog = parser.parse(data);
print(prog)