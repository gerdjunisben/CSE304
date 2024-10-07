# Benjamin Gerdjunis 
# SB ID:
# Net ID:
# Donato Zampini
# SB ID: 114849209
# Net ID: dzampini

import src.decaf_lexer as decaf_lexer
import src.decaf_parser as decaf_parser


data = open('HW3/hw2_testing_subset/5.decaf').read()


prog = decaf_parser.parse(data);
print(prog)