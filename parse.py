import AST
import ply.yacc as yacc
from lex import tokens
import os
import sys
import io

precedence = (
    ('nonassoc', 'SI'),
    ('nonassoc', 'SINON'),
    ('left', 'OU'),
    ('left', 'ET'),
    ('nonassoc', 'EGAL', 'NOT_EQUAL', 'SUP', 'INF', 'GREATERTHENEQUAL', 'LESSTHENEQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLIE', 'DIVISE'),
    ('right', 'UMINUS', 'UPLUS'),
    ('nonassoc', 'NON')
)

def p_start(p):
    '''start : program'''
    p[0] = p[1]
    print("accepted")

def p_program_rec(p):
    '''program : function program'''
    p[0] = AST.ProgramNode([p[1]] + p[2].children)

def p_program_main(p):
    '''program : function_main'''
    p[0] = AST.ProgramNode([p[1]])

def p_function(p):
    '''function : ENTIER ID PAR_OUV para_func PAR_FER declaration ACCO_OUV instrwithreturn ACCO_FER
                | ID PAR_OUV para_func PAR_FER declaration ACCO_OUV instructions ACCO_FER'''
    if len(p) == 9:
        p[0] = AST.FunctionNode(AST.TokenNode(p[2]), [p[8]])
    else:
        p[0] = AST.FunctionNode(AST.TokenNode(p[1]), [p[7]])

def p_function_main(p):
    '''function_main : MAIN PAR_OUV PAR_FER declaration ACCO_OUV instructions ACCO_FER'''
    p[0] = AST.FunctionNode(AST.TokenNode(p[1]), [p[6]])

def p_para_func(p):
    '''para_func : ENTIER ID VIRGULE para_func
                 | ENTIER ID CROCH_OUV CROCH_FER
                 | ENTIER ID CROCH_OUV CROCH_FER VIRGULE para_func
                 | ENTIER ID
                 | empty'''

def p_declaration(p):
    '''declaration : ENTIER ID VIRGULE declaration
                   | ENTIER ID VIRGULE list_id POINT_VIRGULE
                   | ENTIER ID CROCH_OUV CROCH_FER VIRGULE declaration
                   | ENTIER ID POINT_VIRGULE
                   | ENTIER ID CROCH_OUV CROCH_FER POINT_VIRGULE
                   | ENTIER ID CROCH_OUV CROCH_FER VIRGULE list_id POINT_VIRGULE
                   | empty'''

def p_list_id_declaration(p):
    '''list_id : ID VIRGULE list_id
               | ID CROCH_OUV CROCH_FER VIRGULE list_id
               | ID
               | ID CROCH_OUV CROCH_FER'''

def p_instructions(p):
    '''instructions : instruction_list
                    | empty'''
    p[0] = AST.BlockNode(p[1])

def p_instrwithreturn(p):
    '''instrwithreturn : instruction_list return_instruction'''
    p[0] = AST.BlockNode(p[2] + p[3])

def p_return_function_exp(p):
    '''return_instruction : RETOUR expression POINT_VIRGULE'''
    p[0] = [AST.ReturnNode(p[2])]

def p_instruction_list(p):
    '''instruction_list : instruction instruction_list
                        | instruction'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_instruction_assign(p):
    '''instruction : ID CROCH_OUV expression CROCH_FER ASSIGN expression POINT_VIRGULE
                   | ID ASSIGN expression POINT_VIRGULE'''
    if len(p) == 5:
        p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])
    else:
        p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3], p[6]])

def p_instruction_if_else(p):
    '''instruction : SI expression ALORS ACCO_OUV instructions ACCO_FER
                   | SI expression ALORS ACCO_OUV instructions ACCO_FER SINON ACCO_OUV instructions ACCO_FER'''
    if len(p) == 7:
        p[0] = AST.IfElseNode([p[2], p[5]])
    else:
        p[0] = AST.IfElseNode([p[2], p[5], p[9]])

def p_instruction_while(p):
    '''instruction : TANTQUE expression FAIRE ACCO_OUV instructions ACCO_FER'''
    p[0] = AST.WhileNode([p[2], p[5]])

def p_instruction_lire(p):
    '''instruction : LIRE PAR_OUV ID PAR_FER POINT_VIRGULE'''
    p[0] = AST.ReadNode(AST.TokenNode(p[3]))

def p_instruction_ecrire_exp(p):
    '''instruction : ECRIRE PAR_OUV expression PAR_FER POINT_VIRGULE'''
    p[0] = AST.PrintNode(p[3])

def p_instruction_ecrire_string(p):
    '''instruction : ECRIRE PAR_OUV STRING PAR_FER POINT_VIRGULE'''
    p[0] = AST.PrintNode(AST.TokenNode(p[3]))

def p_instruction_function_call(p):
    '''instruction : function_call POINT_VIRGULE'''

def p_expression_bin(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression OU expression
                  | expression EGAL expression
                  | expression LESSTHENEQUAL expression
                  | expression NOT_EQUAL expression
                  | expression MULTIPLIE expression
                  | expression DIVISE expression
                  | expression INF expression
                  | expression SUP expression
                  | expression ET expression
                  | expression GREATERTHENEQUAL expression'''
    p[0] = AST.BinOpNode(p[2], [p[1], p[3]])

def p_expression_replace(p):
    '''expression : NUMBER
                  | ID'''
    p[0] = AST.TokenNode(p[1])

def p_expression_paren(p):
    '''expression : PAR_OUV expression PAR_FER'''
    p[0] = p[2]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = AST.BinOpNode(p[1], [p[2]])

def p_expression_uplus(p):
    'expression : PLUS expression %prec UPLUS'
    p[0] = AST.BinOpNode(p[1], [p[2]])

def p_expression_not(p):
    'expression : NON expression %prec NON'
    p[0] = AST.BinOpNode(p[1], [p[2]])

def p_function_call(p):
    '''function_call : ID PAR_OUV expression_list PAR_FER'''

def p_expression_list(p):
    '''expression_list : expression VIRGULE expression_list
                       | expression
                       | empty'''

def p_empty(p):
    '''empty :'''

def p_error(p):
    print('not accepted')
    #raise SyntaxError(f"Syntax error '{p.value}' in line {p.lineno}")

def parse(program):
    # Create a string buffer to capture the output
    output_buffer = io.StringIO()

    # Redirect the standard output to the buffer
    sys.stdout = output_buffer

    # Call yacc.parse to parse the program
    result = yacc.parse(program)

    # Restore the standard output
    sys.stdout = sys.__stdout__

    # Get the output as a string
    output = output_buffer.getvalue()

    # Close the buffer
    output_buffer.close()

    # Return the parsed result and the captured output
    return result, output

import sys

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
generated_dir = os.path.join(current_directory, "generated")

yacc.yacc(outputdir=generated_dir)

def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Error: missing file argument")
        sys.exit(1)

    filename = sys.argv[1]
    prog = read_file(filename)
    result, output = parse(prog)
    print(output)
