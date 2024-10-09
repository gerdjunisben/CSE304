import os

import decaf_checker as checker


# Format of triples: (<test number>, <test name>, <test result>)
#########NOTE That I took and edited some of these test from the decaf repo on git in case some of
#########these feel familiar, they are good strong samples and saved a ton of time
tests = [
         ('1', 'class -> ...', 'YES'),
         ('2', 'class_body_decl -> field_decl', 'YES'),
         ('3', 'class_body_decl -> constructor_decl', 'YES'),
         ('4', 'class_body_decl -> method_decl', 'YES'),
         ('5', 'stmt -> var_decl', 'YES'),
         ('6', 'method_decl -> ...', 'YES'),
         ('7', 'Same as 6', 'YES'),
         ('8', 'stmt -> while, stmt_list -> stmt+', 'YES'),
         ('9', 'stmt -> if', 'YES'),
         ('10', "primary -> new id '(' ')'", 'YES'),
         ('11', 'stmt -> stmt_expr -> assign', 'YES'),
         ('12', 'lhs -> field_access', 'YES'),
         ('13', 'stmt -> for', 'YES'),
         ('14', 'comment', 'YES'),
         ('15', 'modifier -> ...', 'YES'),
         ('16', 'various math test', 'YES'),
         ('17', 'for loop test', 'YES'),
         ('18', 'boolean ops test', 'YES'),
         ('19', 'fib test1', 'YES'),
         ('20', 'fib test2', 'YES'),
         ('21', 'various expressions test','YES'),
         ('22', 'multiclass and inheritance test','YES'),
         ('err1', "error: eof in class declaration", 'ERROR'),
         ('err2', "error: int const class name", 'ERROR'),
         ('err3', "error: missing type for formal param", 'ERROR'),
         ('err4', "error: gobbledy gook", 'ERROR'),

]
def run_tests(tests):
    for test_number, test_name, test_result in tests:
        path = os.path.join("HW3/hw2_testing_subset",f"{test_number}.decaf")
        print(f"Running test: {test_name} Expected Result: {test_result}")
        
        checker.check(path)

if __name__ == "__main__":
    run_tests(tests)