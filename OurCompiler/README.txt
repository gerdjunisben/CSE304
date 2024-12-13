Benjamin Gerdjunis 
SB ID: 115962358
Net ID: bgerdjunis
Donato Zampini
SB ID: 114849209
Net ID: dzampini


Final report:
Some earlier printing parts may not work cause we ended up make some bug fixes but you know
the compiler works so it doesn't really matter. Note the file it produces will be in the
same dir as the open file and as requested the name will be different. At the top of the
compiled file is the static allocated area and then all the functions. In decaf_absmc is
the StorageMachine which handles labels and registers and contains classes for
instructions, decaf_codegen does all the work
with compiling and decaf_compiler just parses and passes.

Update: Put the print and scan stuff in a file that is "linked" in, you will notice we got
4 print labels well 

"Assume that in each class, there is at most one constructor and at
most one method with a given name. Also assume that the names of methods defined in a class are
distinct from method names in its super classes. You do not need to check for these constraints. Your
type checker can safely assume that they are true."

So I'm not gonna fix that because I don't have to and I have stuff to do tomorrow.

Update: Nevermind also I forgot to note that I use the first two temp registers to hold 1 and 0 because
they get used so often and MIPS did it so I thought I'd save a few instructions.



src:
    decaf_absmc:
        Contains definitions of instruction classes as well as a class that handles registers
        and label distribution
    decaf_codegen:
        Generates instructions from a decaf file block by block (after parsing, typechecking and junk)
        and returns a string of the instructions.
    decaf_compiler:
        Takes a decaf file on command line and creates an ami
    decaf_ast.py:      
        contains the classes for our AST and the printer/error checker

    decaf_scoper.py:    
        contains the classes for the scoper which tracks scope during parsing and handles adding names
        to scopes.

    decaf_typecheck.py:
        contains the classes for the type checker that tracks the type hierarchy and checks types
        according to various constraints

    decaf_lexer.py:    
        this file containts the lexical rules for our language
    
    decaf_parser.py: 
        this file containts the parser rules for our language
    
    decaf_checker.py:
        This file uses the parser and lexer to check if a file given in argv[1] contains a valid program and also produces a parse tree. The parse tree could use some work but it seems to accept the language just leaves a few nones.

    tests.py:
        This runs the tests in the hw2_testing_subset folder. Note that it uses colorama to make passed tests green and failed tests red, if it doesn't work for whatever reason included are normal prints commented out

    parser.out:
        The output when the parser is formed

    parsetab.py:
        Contains the fully formed parse

parser.out:
Auto-generated file created by PLY that prints out the logistics of the parser, including unused terminals, grammar rules, and parser structure

parsetab.py:
Auto-generated file that shows a consolidated version of the lexer and the parser