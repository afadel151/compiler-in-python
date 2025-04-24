import ply.yacc as yacc
from lex import tokens
import AST
###############################################################################
success_value = 1

operations = {
        '+': lambda x, y: x+y,
        '-': lambda x, y: x-y,
        '*': lambda x, y: x*y,
        '/': lambda x, y: x / y,
        '&&' : lambda x, y : x & y,
        '||' : lambda x, y : x|y,
        '<' : lambda x, y : x < y,
        '>' : lambda x, y : x > y,
        '>=' : lambda x, y: x >= y,
        '<=' : lambda x, y: x <= y,
        '==' : lambda x, y: x == y,
        '!=' : lambda x, y: x != y
}

precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUAL', 'INEQUAL'),
    ('left', 'LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL'),
    ('left', 'NOT')
)

###############################################################################
# Initialisation de la variable current_line
#current_line = 1
#
#def p_newline(p):
#    """
#    newline : '\n'
#    """
#    global current_line
#    current_line += 1
#    # Mettre à jour la variable lineno de l'objet p
#    p.lineno = current_line
  
def parse(prog):
    yacc.yacc(outputdir='generated')
    return yacc.parse(prog)


def p_error(p):
    global success_value
    if p:
        print(f"Syntax error at token {p.type} ({p.value}) on line {p.lineno} at rule '{p.type}'")
        
    else:
        print("Syntax error at EOF")
    success_value = -1
    # Raise an exception to stop parsing

###############################################################################
#def p_axiome(p):
#    '''axiome : library_directive_list debut '''
#    p[0] = (p[1],p[2])
#    print('PROGRAMME COMPILE AVEC SUCCES !')  
#    
#    
#def p_library_directive_list(p):
#    '''library_directive_list : library_directive
#                              | library_directive_list library_directive
#    '''
#    if len(p) == 2:
#        p[0] = [p[1]]
#    else:
#        p[1].append(p[2])
#        p[0] = p[1]
#
#def p_library_directive(p):
#    '''library_directive : INCLUDE LIBRARY_NAME
#    '''
#    p[0] = p[2]

    
###############################################################################  

    
def p_debut(p):
    '''debut : function_declaration debut
             | main
             | instruction_list'''
    print('PROGRAMME COMPILE AVEC SUCCES !')
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = AST.ProgramNode([p[1],p[2]])

###############################################################################
def p_main(p):
    '''main : MAIN LPAREN RPAREN LBRACE instruction_list RBRACE
            | MAIN LPAREN RPAREN list_dec LBRACE instruction_list RBRACE
            | ENTIER MAIN LPAREN list_dec RPAREN LBRACE instruction_list retour_expression RBRACE
            '''

    if len(p) == 7:
        p[0] = p[5]
#    elif len(p) == 8:
#        p[0] = p[6]
    elif len(p) == 10 :
        p[0] = AST.ProgramNode([p[4],p[7],p[8]])
    else:
        p[0] = AST.ProgramNode([p[4],p[6]])
    #print("main executer avec succé")     
  
###############################################################################    
    
def p_function_declaration(p):
    '''function_declaration : ID LPAREN list_dec RPAREN list_dec LBRACE instruction_list retour_expression RBRACE'''
    p[0] = (p[3], p[5], p[7], p[8])
    

############################################################################## 
     
def p_function_call(p):
    '''function_call : ID LPAREN argument_list RPAREN '''
    p[0] = p[3]
    
    
###############################################################################
    
def p_argument_list(p):
    '''argument_list : ID
                     | NUMBER
                     | argument_list COMMA ID
                     | argument_list COMMA NUMBER'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]
      
###############################################################################
    
def p_retour_expression(p):
    '''retour_expression : RETOUR instruction POINT_VIRG'''
    p[0] = AST.ReturnNode([p[2]])
   
###############################################################################
    
def p_list_dec(p):
    '''list_dec : ENTIER list_id POINT_VIRG
                | ENTIER list_id'''
    p[0] = p[2]

###############################################################################
    
def p_list_id(p):
    '''list_id : ID
               | list_id COMMA ID
               | list_id COMMA ENTIER ID
               | ID ARRAY
               | list_id COMMA ID ARRAY
               | list_id COMMA ENTIER ID ARRAY'''
    if len(p) > 3 :
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = AST.TokenNode(p[1])

############################################################################### 
    
def p_instruction_list(p):
    '''instruction_list : instruction 
                        | instruction_list instruction''' 
    if len(p) == 2:
        p[0] = AST.ProgramNode([p[1]])
    else:
        p[0] = AST.ProgramNode([p[1] , p[2]])
    #print("instruction list reconue avec succé")
    
###############################################################################
  
def p_expression_assign(p):
    '''expression_assign : ID ASSIGNMENT expression_arth 
                         | ID ASSIGNMENT expression_log
                         | ID ASSIGNMENT function_call
   '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]) , p[3]])
    #print("ASSIGN executer avec succé")
    
###############################################################################       

def p_instruction (p):
    '''instruction :  if_exprs POINT_VIRG
                    | if_exprs
                    | si_exprs POINT_VIRG
                    | si_exprs
                    
                    | while_exprs
                    | while_exprs POINT_VIRG
                    
                    | ecrire_msg POINT_VIRG
                    | lire_msg POINT_VIRG
                    | ecrire_msg
                    | lire_msg

                    | expression_arth
                    | expression_log
                    | expression_compare
                    | expression_assign POINT_VIRG
                    | expression_assign
                    | expression_uminus
                
                    '''
    p[0] = p[1]
 
    #print("instruction recconu succé")

###############################################################################
       
def p_ecrire_msg(p):
    '''ecrire_msg : ECRIRE LPAREN expression_arth RPAREN
                  | PRINT LPAREN expression_arth RPAREN'''
    p[0] = AST.PrintNode([p[3]])
    #print("ecrire message avec succé")
 
###############################################################################
      
def p_lire_msg(p):
    '''lire_msg : LIRE LPAREN ID RPAREN '''
    p[0] = AST.ReadNode([AST.TokenNode(p[3])])
    #print("lire message avec succé")

###############################################################################
    
def p_expression_arth(p):
    '''expression_arth : expression_arth ADD_OP expression_arth
                       | expression_arth MUL_OP expression_arth
                       
                       | expression_uminus
                       | token
                       | paren_expression_arth'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        print(p[2])
        p[0] = AST.OpNode(p[2], [p[1], p[3]])
    #print("expr arth avec succé")
    
###############################################################################  
    
def p_token(p):
    '''token : NUMBER
             | ID
             | STRING
             | CHARACTER'''
    p[0] = AST.TokenNode(p[1])
    
    
###############################################################################
    
def p_if_exprs(p):
    '''if_exprs : IF  expression_log  ALORS_MAJ LBRACE instruction_list RBRACE
                | IF  LPAREN expression_log RPAREN LBRACE instruction_list RBRACE 
                | IF  expression_log  ALORS_MAJ LBRACE instruction_list RBRACE SINON LBRACE instruction_list RBRACE'''
    if len(p) == 8:
        p[0] = AST.IfNode([p[3],p[6]])
    elif len(p) == 7:
        p[0] = AST.IfNode([p[2],p[5]])
    elif len(p) == 11:
        p[0] = AST.IfNode([p[2],p[5],p[9]])
    #print('if alors')
    
def p_si_exprs(p):
    '''si_exprs : SI  expression_log  ALORS_MIN LBRACE instruction_list RBRACE
                | SI  expression_log  ALORS_MIN LBRACE instruction_list RBRACE SINON LBRACE instruction_list RBRACE
                | SI  LPAREN expression_log RPAREN  ALORS_MIN LBRACE instruction_list RBRACE
                | SI  LPAREN expression_log RPAREN ALORS_MIN LBRACE instruction_list RBRACE SINON LBRACE instruction_list RBRACE'''
    if len(p) == 7:
        p[0] = AST.IfNode([p[2],p[5]])
    elif len(p) == 11:
        p[0] = AST.IfNode([p[2],p[5],p[9]])
        #print('si sinon')
    elif len(p) == 9:
        p[0] = AST.IfNode([p[3],p[7]])
    else:
        p[0] = AST.IfNode([p[3],p[7],p[11]])
       
    

############################################################################### 
    
def p_while_exprs(p):
    '''while_exprs : WHILE LPAREN expression_log RPAREN LBRACE instruction_list RBRACE
                | TANTQUE LPAREN expression_log RPAREN ALORS_MIN LBRACE instruction_list RBRACE
                | TANTQUE expression_log ALORS_MAJ LBRACE instruction_list RBRACE
                | TANTQUE expression_log ALORS_MIN LBRACE instruction_list RBRACE
                | TANTQUE expression_log FAIRE LBRACE instruction_list RBRACE
                | TANTQUE LPAREN expression_log RPAREN FAIRE LBRACE instruction_list RBRACE
                '''
    if len(p) == 8:
        p[0] = AST.WhileNode([p[3],p[6]])
    elif len(p) == 9:
        p[0] = AST.WhileNode([p[3],p[7]])
    else:
        p[0] = AST.WhileNode([p[2],p[5]])
    #print("while avec succé")
    
###############################################################################
    
def p_expression_log(p):
    '''expression_log : expression_log AND expression_log
                      | expression_log OR expression_log
                      | expression_compare
                      | NOT LPAREN expression_log RPAREN
                      '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p)== 5:
        p[0] = AST.OpNode(p[1], [p[3]])
    else:
        p[0] = AST.OpNode(p[2], [p[1],p[3]])
    #print("expression log reconu avec succé")
        
###############################################################################    
def p_expression_compare(p):
    '''expression_compare : expression_arth GREATER expression_arth 
                            | expression_arth LESS expression_arth 
                            | expression_arth GREATER_EQUAL expression_arth 
                            | expression_arth LESS_EQUAL expression_arth 
                            | expression_arth EQUAL expression_arth
                            | expression_arth INEQUAL expression_arth
                            | expression_arth NOT expression_arth
                            '''
    p[0] = AST.OpNode(p[2], [p[1],p[3]])
    #print("expression compare reconu avec succé")
    
###############################################################################    
def p_paren_expression_arth(p):
    '''paren_expression_arth : LPAREN expression_arth RPAREN
                       '''
    p[0] = p[2]
    #print("expr arth parenth avec succé")
    
###############################################################################
    
def p_expression_uminus(p):
    'expression_uminus : ADD_OP expression_arth %prec UMINUS'
    if p[1]=='-':
        #p[0] = -int(p[2])
        p[0] = AST.OpNode("-", [0,p[2]])
    else:
        p[0] = int(p[2])

    #print("expression uminus reconu avec succé")

###############################################################################
#        
#def p_while_exprs(p):
#    '''while_exprs : WHILE LPAREN expression_log RPAREN LBRACE instruction_list RBRACE POINT_VIRG'''
#    p[0] = ('while', p[3], p[6])
#   
#
################################################################################
#    
#def p_for_exprs(p):
#    '''for_exprs : FOR LPAREN expression_assign POINT_VIRG expression_log POINT_VIRG expression_assign RPAREN LBRACE instruction_list RBRACE '''
#    p[0] = ('for', p[3], p[4], p[5], p[8])
#    
#    #print("for_exp reconu avec succé")
################################################################################
#    
#def p_do_while_exprs(p):
#    '''do_while_exprs : DO LBRACE instruction_list RBRACE WHILE LPAREN expression_log RPAREN'''
#    p[0] = ('do_while', p[7], p[3])
#  
#    #print("do_while exp reconu avec succé")
###############################################################################
#def p_case_exprs(p):
#    '''case_exprs : CASE instruction DEUX_PTS LBRACE instruction_list RBRACE'''
##    if len(p) == 1:
##        p[0] = p[1]
##    else:
#    p[0] = ('case', p[5], p[2])
#    
#    print("case_exp reconu avec succé")
################################################################################
#def p_switch_case_exprs(p):
#    '''switch_case_exprs : SWITCH LPAREN instruction RPAREN LBRACE case_exprs'''
#    p[0] = ('switch_case', p[6], p[3])
#    
#    print("switch_exp reconu avec succé")
###############################################################################
    
#def p_parameter_list(p):
#    '''parameter_list : ENTIER parameter_declaration
#                      | parameter_list COMMA ENTIER parameter_declaration'''
#    if len(p) == 2:
#        p[0] = [p[1]]
#    else:
#        p[1].append(p[3])
#        p[0] = p[1]
#
#    print("parameter list reconu avec succé")
#    
################################################################################
#    
#def p_parameter_declaration(p):
#    '''parameter_declaration : ID
#                             | ID ARRAY'''
#    p[0] = ('parameter_declaration', p[1], p[2])
#
#    print("parametre dec reconu avec succé")
###############################################################################
        
import sys
#filename = "parser1.txt"
yacc.yacc(outputdir='generated')
def read_file(filename):
    with open(filename, 'r') as file:
        f=(file.read())
    return f

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Error: missing file argument")
        sys.exit(1)
    filename = sys.argv[1]
    prog =read_file(filename)
    print(prog)
    
    result =yacc.parse(prog)
    print(result)
    if success_value > 0:
        print("ACCEPTE")
    else:
        print("REFUSE")