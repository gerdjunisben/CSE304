Benjamin Gerdjunis 
SB ID: 115962358
Net ID: bgerdjunis
Donato Zampini
SB ID: 114849209
Net ID: dzampini

hw2_testing_subset:
    Contains folder of test files for testing the program
    1-15 + err1-err3 are made by mr. Osborne

    16-22 + err4 are made by a mix of me and the decaf repo on git, there are some rules we didn't apply or were not in the doc given so I had to edit most of them to work in our version.
    I mainly took ones I thought were good ideas for tests and built them in the way ours works, I figured I should at least quote my source.
    see it here https://github.com/hawkw/decaf/tree/master


src:
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