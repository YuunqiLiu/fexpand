# Yacc example
from copy import copy, deepcopy
from functools import reduce
import ply.yacc as yacc 
import ply.lex as lex
import os
# Get the token map from the lexer.  This is required.
from .path_record import *
import re

if __name__ == "__main__":
    from path_parser import *
else:
    from .path_parser import *

class AstNode(object):

    def __init__(self):
        self.lineno     = None
        self._value = None

    def get_formatted_value(self):
        return re.sub('\s+',' ',self.value)

class AstExplist(AstNode):

    def __init__(self):
        super().__init__()
        self.son_list = []

    @property
    def value(self):
        return ''.join([x.value for x in self.son_list])
    

    def get_legal_value(self):
        return ''.join(x.get_legal_value() for x in self.son_list)

class AstExp(AstNode):

    def __init__(self):
        super().__init__()
        self._value = None

    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, val):
        self._value = val

    def get_legal_value(self):
        return self.value


class AstFilelist(AstNode):

    def __init__(self):
        super().__init__()
        self.son_list = []

    @property
    def value(self):
        return ''.join([x.value for x in self.son_list])

    @value.setter
    def value(self, val):
        self._value = val

    def get_legal_value(self):
        #if PathRecord.check_payload_path_duplicate(self):
        #    res = ''
        #else:
        if os.path.exists(self.value):
            res = self.value
            if PathRecord.check_payload_filename_duplicate(self):
                res = ''
            else:
                res = self.value
                PathRecord.PAYLOAD_FILENAME_LIST.append(self)
        else:
            res = self.value
            print(f'[Error] Skip conflict check for file {self.value} at {PathRecord.CURRENT_FILE}:{self.lineno} because it is not exist, .')
        PathRecord.PAYLOAD_PATH_LIST.append(self)

        return res



class AstFile(AstNode):

    def __init__(self):
        super().__init__()
        self._value = None

    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, val):
        self._value = val

##########################################################################################################


##########################################################################################################

def p_expression_lst_create(p):
    '''
    exp_list : expression
             | file_list
    '''
    p[0] = AstExplist()
    p[0].lineno = p[1].lineno
    p[0].son_list.append(p[1])
    p[0].file = PathRecord.CURRENT_FILE

def p_expression_lst_append(p):
    '''exp_list : exp_list expression
                | exp_list file_list'''
    p[0] =  deepcopy(p[1])
    p[0].son_list.append(p[2])

#def p_expression_basic(p):
#    'expression : file_name'

    # p[1].file = PathRecord.CURRENT_FILE
    # if not PathRecord.check_payload_path_duplicate(p[1]):
    #     #PathRecord.PAYLOAD_PATH_LIST.append(p[1])
    #     if os.path.exists(p[1].value):
    #         abs_path = os.path.abspath(p[1].value)
    #         p[0] = abs_path

    #         new_dir, new_name = os.path.split(p[1].value)

    #         for old_path in PathRecord.PAYLOAD_PATH_LIST:
    #             old_dir, old_name = os.path.split(old_path.value)
    #             if new_name == old_name:
    #                 conflict = not filecmp.cmp(p[1].value, old_path.value)

    #                 if conflict:
    #                     print(f'[Conflict] {p[1].value} in {p[1].file}:{p[1].lineno} has diff content with {old_path.value} in {old_path.file}:{old_path.lineno}, skip.')
    #                 else:
    #                     print(f'[Warning] {p[1].value} in {p[1].file}:{p[1].lineno} has same content with {old_path.value} in {old_path.file}:{old_path.lineno}, skip.')
    #                 p[0] = ''
    #              
    #     else:
    #         print(f'[Warning] File {p[1].value} at {PathRecord.CURRENT_FILE}:{p[1].lineno} not exist, skip conflict check and pass through to output.')
    #         p[0] = p[1].value
    # else:
    #     p[0] = ''
    #print(p[0])

    # if os.path.exists(p[1].value):
    #     abs_path = os.path.abspath(p[1].value)
# # # 
    #     p[1].file = PathRecord.CURRENT_FILE
    #     if PathRecord.check_payload_path_duplicate(p[1]):
    #         p[0] = ''
    #     else:
    #         p[0] = abs_path
    #         #PathRecord.PAYLOAD_PATH_LIST.append(p[1])
    # else:
    #     print(f'[Warning] File {p[1].value} at {PathRecord.CURRENT_FILE}:{p[1].lineno} not exist, but pass through to output.')
    #     p[0] = p[1].value
    #print(p[0])



def p_file_list_create(p):
    'file_list : file_name'
    p[0] = AstFilelist()
    p[0].lineno = p[1].lineno
    p[0].son_list.append(p[1])
    p[0].file = PathRecord.CURRENT_FILE


def p_file_list_merge(p):
    'file_list : file_list file_name'
    p[0] = deepcopy(p[1])
    p[0].son_list.append(p[2])
    p[0].file = PathRecord.CURRENT_FILE



def p_filename_init(p):
    '''file_name : CPP_FSLASH
                 | CPP_ID
                 | CPP_INTEGER
                 | CPP_DOT
                 | CPP_MINUS
    '''
    p[0] = AstFile()
    p[0].lineno = p.lineno(1)
    p[0].value  = p[1]



def p_env_expand_(p):
    'file_name : CPP_ENV'

    p[0] = AstFile()
    p[0].lineno = p.lineno(1)
    p[0].value  = p[1]
    
    if not p[1] in os.environ:
        print(f'Error at {PathRecord.CURRENT_FILE}:{p.lineno(1)}, env var {p[1]} not exist, keep it.')
        p[0].value = p[1]
    else:
        p[0].value = os.environ[p[1]]
        



    # p[0] = AstNode()
    # p[0].type   = 'PATH'
    # p[0].lineno = p.lineno(1)
    # p[0].value  = p[1].value + p[2].value
    #p[0] = p[1] + p[2] 


# def p_file_name_cpp_id(p):
#     'file_name : CPP_ID'
#     p[0] = AstFile()
#     p[0].lineno = p.lineno(1)
#     p[0].value  = p[1]
# 
# 
# def p_file_name_cpp_integer(p):
#     'file_name : CPP_INTEGER'
#     p[0] = AstFile()
#     p[0].lineno = p.lineno(1)
#     p[0].value  = p[1]
# 
# 
# 
# 
# def p_file_name_cpp_dot(p):
#     '''
#     file_name : CPP_DOT
#               | CPP_MINUS'''
#     p[0] = AstFile()
#     p[0].lineno = p.lineno(1)
#     p[0].value  = p[1]
# 
#     #p[0] = p[1]



def p_exp_plus_id_plus(p):
    '''expression : CPP_PLUS CPP_ID
                  | CPP_MINUS CPP_ID
    '''
    p[0] = AstExp()
    p[0].lineno = p.lineno(1)
    p[0].value  = p[1] + p[2]



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
    p[0] = AstExp()
    p[0].lineno = p.lineno(1)
    p[0].value  = p[1]




# Error rule for syntax errors
def p_error(p):
    #print(p)
    print("Syntax error in input %s !" % p)

# Build the parser

#print(res)

lexer = default_lexer()
pathparser = yacc.yacc(debug=1)


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
