import ply.lex as lex
import sys

#les lexemes simples
t_ADD_OP=r'\+|\-'
t_MUL_OP=r'\*|/'
t_LPAREN=r'\('
t_RPAREN=r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_AND=r'&'
t_OR=r'\|'
t_ignore_COMMENT = r'\#.*' #t_ignore reserver par lex.py pour ignore les trucs specifier
t_POINT_VIRG = r';'
t_BLANC = r'\s' #definie mais non ajouter a la liste des tokens pour les ignoré
t_ASSIGNMENT = r'='
t_EQUAL = r'=='
t_INEQUAL = r'!='
t_GREATER = r'>'
t_LESS = r'<'
t_GREATER_EQUAL = r'>='
t_LESS_EQUAL = r'<='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_CHARACTER = r'\'[^\']*\''
t_STRING = r"\'[^\"]*\'"
t_COMMA = r','
t_NOT = r'!'
#t_MODULO = r'%'
t_ignore = ' \t\n'
#t_DEUX_PTS = r':'
#t_DUBLE_QUOTE = r'\"'
#t_QUOTE = r"\'"
#t_LIBRARY_NAME = r'\w +'
t_ARRAY = r'\[[^\]]*\]'

#t_VIRGULE= '\.'



current_line = 1


#Instruction
reserved = {
    'main' : 'MAIN',
    'ecrire' : 'ECRIRE',
    'lire' : 'LIRE',
    'print' : 'PRINT',
    'if' : 'IF',
    'si' : 'SI',
    'alors' : 'ALORS_MIN',
    'Alors' : 'ALORS_MAJ',
    'sinon' : 'SINON',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'tantque' : 'TANTQUE',
    #'for' : 'FOR',
    #'do' : 'DO',
    #'switch' : 'SWITCH',
    #'case' : 'CASE',
    #'default' : 'DEFAULT',
    #'break' : 'BREAK',
    #'continue' : 'CONTINUE',
    'retour' : 'RETOUR',
    #'struct' : 'STRUCT',
    'function' : 'FUNCTION',
    'entier' : 'ENTIER',
    'faire' : 'FAIRE'
    }

tokens = [
        'ADD_OP', 
        'MUL_OP',
        'NUMBER',
        'ID',          
        'newline',
        'LPAREN',
        'RPAREN',
        'LBRACE',
        'RBRACE',
        'AND',
        'OR',
        'ignore_COMMENT',
        'POINT_VIRG',
        'BLANC',
        'ASSIGNMENT',
        'EQUAL',
        'INEQUAL',
        'GREATER',
        'LESS',
        'GREATER_EQUAL',
        'LESS_EQUAL',
        'LBRACKET',
        'RBRACKET',
        'CHARACTER',
        'STRING',
        'COMMA',
        'NOT',
        'ARRAY'
        ] + list(reserved.values())
###############################################################################
def t_NUMBER(t):
    r'\d+(\.\d+)?'   # mettre à jour la règle pour reconnaître les nombres flottants
    if '.' not in t.value:
        t.value = int(t.value)
    else:
        t.value = float(t.value)
    return t
###############################################################################
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)   
###############################################################################
#afin de comparer si c'est un ID ou un mot qui appartient a reserved list
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    t.lineno = current_line
    return t
###############################################################################
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1
###############################################################################
def t_error(t):
    global success_value
    print("Erreur de syntaxe : '%s', ligne %d" % (t.value[0], current_line))
    success_value = -1
    t.lexer.skip(1)
###############################################################################
def read_file(filename):
    with open(filename, 'r') as file:
        f=(file.read())
    return f
###############################################################################
success_value = 1
lexer= lex.lex()
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Error: missing file argument")
        sys.exit(1)
    filename = sys.argv[1]
    prog =read_file(filename)
    print(prog)


    # lex.input( prog )
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break # No more input
    #     print(tok)
    # if success_value > 0:
    #     print("ACCEPTE")
    # else:
    #     print("REFUSE")

