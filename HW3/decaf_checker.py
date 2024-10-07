import decaf_lexer
import decaf_parser


data = open('HW3/hw2_testing_subset/5.decaf').read()


prog = decaf_parser.parse(data);
print(prog)