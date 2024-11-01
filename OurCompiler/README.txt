Benjamin Gerdjunis 
SB ID: 115962358
Net ID: bgerdjunis
Donato Zampini
SB ID: 114849209
Net ID: dzampini


A4 report:
Yeah, we didn't quite finish, midterms kinda hit us both like two conveintly well timed trucks.
Anyways the parser makes as much of the AST as it can or at least I think it does (Ben).
We started the printer/error checker but didn't quite finish it, it doesn't print fully but
we're working on it, you can see the base stuff in check and you can see the recursive bits in
createPrintRecurr. The error checking does not do scope or dup fields yet. We don't fill in all
additional info yet such as id on access but we do get field classname. We're gonna finish in
the coming days and then we'll be ready for the next part.


hw2_testing_subset:
    Contains folder of test files for testing the program
    1-15 + err1-err3 are made by mr. Osborne

    16-22 + err4 are made by a mix of me and the decaf repo on git, there are some rules we didn't apply or were not in the doc given so I had to edit most of them to work in our version.
    I mainly took ones I thought were good ideas for tests and built them in the way ours works, I figured I should at least quote my source.
    see it here https://github.com/hawkw/decaf/tree/master


src:
    decaf_ast.py:      <<<<NEW
        contains the classes for our AST and the printer/error checker
    decaf_lexer.py:    
        this file containts the lexical rules for our language
    
    decaf_parser.py:   <<<<NEW
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