# Yacc example

import ply.yacc as yacc 
import ply.lex as lex
import os
# Get the token map from the lexer.  This is required.
from .path_record import *

if __name__ == "__main__":
    from path_parser import *
else:
    from .path_parser import *
#from pcpp.evaluator import *

class Path(object):

    def __init__(self,value,is_path = True) -> None:
        self.value = value
        self.is_path = is_path

def p_expression_lst_create(p):
    'exp_list : expression'
    p[0] = [p[1]]

def p_expression_lst_append(p):
    'exp_list : exp_list expression'
    p[0] = p[1] + [p[2]]



def p_expression_basic(p):
    'expression : file_name'
    if os.path.exists(p[1].value):
        abs_path = os.path.abspath(p[1].value)

        p[1].file = PathRecord.CURRENT_FILE
        if PathRecord.check_payload_path_duplicate(p[1]):
            p[0] = ''
        else:
            p[0] = abs_path
            PathRecord.PAYLOAD_PATH_LIST.append(p[1])
    else:
        print(f'[Warning] File {p[1].value} at {PathRecord.CURRENT_FILE}:{p[1].lineno} not exist, but pass through to output.')
        p[0] = p[1].value

def p_file_name_merge(p):
    'file_name : file_name file_name'
    p[0] = LexToken()
    p[0].type   = p[2].type
    p[0].lineno = p[2].lineno
    p[0].lexpos = 0
    p[0].value  = p[1].value + p[2].value
    #p[0] = p[1] + p[2] 

def p_filename_init(p):
    'file_name : CPP_FSLASH'
    p[0] = LexToken()
    p[0].type   = 'CPP_FSLASH'
    p[0].lineno = p.lineno(1)
    p[0].lexpos = 0
    p[0].value  = p[1]
    #p[0] = '/'

def p_env_expand_(p):
    'file_name : CPP_ENV'

    p[0] = LexToken()
    p[0].type   = 'CPP_ENV'
    p[0].lineno = p.lineno(1)
    p[0].lexpos = 0
    p[0].value  = p[1]
    
    if not p[1] in os.environ:
        print(f'Error at {PathRecord.CURRENT_FILE}:{p.lineno(1)}, ENV {p[1]} not exist.')
        p[0].value = p[1]
    else:
        p[0].value = os.environ[p[1]]
        


def p_file_name_cpp_id(p):
    'file_name : CPP_ID'
    p[0] = LexToken()
    p[0].type   = 'CPP_ID'
    p[0].lineno = p.lineno(1)
    p[0].lexpos = 0
    p[0].value  = p[1]
    #p[0] = p[1]

def p_file_name_cpp_integer(p):
    'file_name : CPP_INTEGER'
    p[0] = LexToken()
    p[0].type   = 'CPP_INTEGER'
    p[0].lineno = p.lineno(1)
    p[0].lexpos = 0
    p[0].value  = p[1]
    #p[0] = p[1]

def p_file_name_cpp_dot(p):
    'file_name : CPP_DOT'
    p[0] = LexToken()
    p[0].type   = 'CPP_DOT'
    p[0].lineno = p.lineno(1)
    p[0].lexpos = 0
    p[0].value  = p[1]

    #p[0] = p[1]

def p_exp_plus_id_plus(p):
    '''expression : CPP_PLUS CPP_ID
                  | CPP_MINUS CPP_ID
    '''
    p[0] = p[1] + p[2]


def p_error_process(p):
    '''
    expression : CPP_AMPERSAND
               | CPP_ANDEQUAL
               | CPP_BAR
               | CPP_BSLASH
               | CPP_CHAR
               | CPP_COLON
               | CPP_COMMA
               | CPP_COMMENT1
               | CPP_COMMENT2
               | CPP_DEREFERENCE
               | CPP_DIVIDEEQUAL
               | CPP_DPOUND
               | CPP_DQUOTE
               | CPP_EQUAL
               | CPP_EQUALITY
               | CPP_EXCLAMATION
               | CPP_FLOAT
               | CPP_GREATER
               | CPP_GREATEREQUAL
               | CPP_HAT
               | CPP_INEQUALITY
               | CPP_LBRACKET
               | CPP_LCURLY
               | CPP_LESS
               | CPP_LESSEQUAL
               | CPP_LINECONT
               | CPP_LOGICALAND
               | CPP_LOGICALOR
               | CPP_LPAREN
               | CPP_LSHIFT
               | CPP_LSHIFTEQUAL
               | CPP_MINUS
               | CPP_MINUSEQUAL
               | CPP_MINUSMINUS
               | CPP_MULTIPLYEQUAL
               | CPP_OREQUAL
               | CPP_PERCENT
               | CPP_PERCENTEQUAL
               | CPP_PLUS
               | CPP_PLUSEQUAL
               | CPP_PLUSPLUS
               | CPP_POUND
               | CPP_QUESTION
               | CPP_RBRACKET
               | CPP_RCURLY
               | CPP_RPAREN
               | CPP_RSHIFT
               | CPP_RSHIFTEQUAL
               | CPP_SEMICOLON
               | CPP_SQUOTE
               | CPP_STAR
               | CPP_STRING
               | CPP_TILDE
               | CPP_WS
               | CPP_XOREQUAL
    '''
    #p[0] = p[1]
    p[0] = p[1]




# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser

#print(res)

lexer = default_lexer()
pathparser = yacc.yacc()


#lexer.input('${QWER}')
#tok_list = [lexer.token(),lexer.token(),lexer.token(),lexer.token()]
#print(tok_list)
if __name__ == "__main__":

    res = pathparser.parse('+incdir+/QWER.QWRE_QWERE.${PATH}.sv/QWER.v')
    print(res)
#res = parser.parse('QWER/ASDF')
# while True:
#    try:
#        s = raw_input('calc > ')
#    except EOFError:
#        break
#    if not s: continue
#    result = parser.parse(s) 
#    print result
