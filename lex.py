import ply.lex as lex
import sys
import os

# Liste des noms des tokens
tokens = (
    'ENTIER',
    'ID',
    'NUMBER',
    'MINUS', 
    'PLUS',
    'MULTIPLIE',
    'NOT_EQUAL',
    'DIVISE',
    'EGAL',
    'INF',
    'SUP',
    'ET',
    'OU',
    'NON',
    'SI',
    'ALORS',
    'RETOUR',
    'TANTQUE',
    'FAIRE',
    'SINON',
    'LIRE',
    'ECRIRE',
    'PAR_OUV',
    'STRING',
    'ASSIGN',
    'PAR_FER',
    'ACCO_OUV',
    'ACCO_FER',
    'CROCH_OUV',
    'VIRGULE',
    'POINT_VIRGULE',
    'MAIN',  
    'CROCH_FER',
    'GREATERTHENEQUAL', 
    'LESSTHENEQUAL'
)


# Expressions régulières pour les tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLIE = r'\*'
t_NOT_EQUAL= r'<>'
t_DIVISE = r'/'
t_EGAL = r'=='
t_INF = r'<'
t_SUP= r'>'
t_ET = r'&'
t_OU = r'\|'
t_MAIN = r'^main\b'
t_NON = r'!'
t_SI = r'si\b'
t_ALORS = r'alors\b'
t_RETOUR = r'^retour\b'
t_TANTQUE = r'^tantque\b'
t_FAIRE = r'faire\b'
t_SINON = r'sinon\b'
t_LIRE = r'^lire\b'
t_ECRIRE = r'^ecrire\b'
t_ENTIER = r'^entier\b'
t_PAR_OUV = r'\('
t_PAR_FER = r'\)'
t_ACCO_OUV = r'\{'
t_ACCO_FER = r'\}'
t_CROCH_OUV = r'\['
t_CROCH_FER = r'\]'
t_VIRGULE = r','
t_POINT_VIRGULE = r';'
t_GREATERTHENEQUAL= r'>='
t_LESSTHENEQUAL=r'<='
t_STRING = r'\'.*\''
t_ASSIGN = r'='
    

    # Fonction pour les identificateurs
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_-]*'
    keywords  = {
        'si': 'SI',
        'alors': 'ALORS',
        'sinon': 'SINON',
        'tantque': 'TANTQUE',
        'faire': 'FAIRE',
        'retour': 'RETOUR',
        'lire': 'LIRE',
        'ecrire': 'ECRIRE',
        'main'  : 'MAIN',
        'entier': 'ENTIER'
    }
    if t.value.lower() in keywords:
        t.type = t.value.upper()
    else:
        t.type = 'ID'
    return t
def t_NOMBRE_SUIVI_IDENTIFICATEUR(t):
    r'\d+[a-zA-Z_][a-zA-Z0-9_]*'
    #print("Erreur : nombre suivi immédiatement d'un identificateur '%s'" % t.value)
    t.lexer.skip(len(t.value))
    print ("not accepted")
    exit(1)


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t
def t_ignore_COMMENTAIRE(t):
    r'\#.*'
    pass

# Caractères à ignorer
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    #print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    print ("not accepted")
    exit(1)


# Fonction pour lire un fichier
def read_file(filename):
    if not os.path.isfile(filename):
        print("Erreur : Le fichier", filename, "n'existe pas.")
        sys.exit(1)
    with open(filename, 'r') as file:
        content = file.read()
    return content

# Création de l'analyseur lexical
lexer = lex.lex()

if __name__ == '__main__':
    # Vérification des arguments en ligne de commande
    if len(sys.argv) != 2:
        print("Erreur : fichier manquant en argument")
        sys.exit(1)
    
    filename = sys.argv[1]
    prog = read_file(filename)
    
    # Utilisation de l'analyseur lexical sur le contenu du fichier
    lexer.input(prog)
    while True:
        tok = lexer.token()
        if not tok:
            break  # Plus d'entrée

       
    print("accepted")
