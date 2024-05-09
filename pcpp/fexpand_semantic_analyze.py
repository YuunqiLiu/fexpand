
import copy
from ply.lex import LexToken
from .path_record import PathRecord

def include_semantic_analyze(ast):
    # create a dummy token to adapt to init pcpp.
    token = LexToken()
    token.type    = 'CPP_PATH'
    token.lineno  = ast.lineno
    token.lexpos  = 0
    token.value   = ast.value.replace('\n','')
    token.file    = PathRecord.CURRENT_FILE
    

    # check include path exist.
    if not PathRecord.check_include_path_exist(token):
        #print(f'[Error-IPNE] Skip include path {token.value} at {PathRecord.CURRENT_FILE}:{token.lineno} because it is not exist.')
        return None

    # check include path duplicate.
    if PathRecord.check_include_path_duplicate(token):
        return None

    # include filelist.
    PathRecord.include(token)
    
      
    # record res in INCLUDE_PATH_LIST
    new_res = copy.copy(token)
    PathRecord.INCLUDE_PATH_LIST.append(new_res)

    # update dummy token 
    token.type = "CPP_STRING"
    token.value = f'\"{token.value}\"'

    return token


def payload_semantic_analyze(ast):
    # create a dummy token to adapt to init pcpp.
    token = LexToken()
    token.type    = 'CPP_PATH'
    token.lineno  = ast.lineno
    token.lexpos  = 0
    token.value   = "" 
    token.file    = PathRecord.CURRENT_FILE

    # ignore all space tokens.
    if ast.value.isspace():
        return [token]

    # Check if the current path is a duplicate of a previous path.
    if PathRecord.check_payload_path_duplicate(ast):
        return [token]
    
    # Check if the current file is a duplicate of a previous file.
    if PathRecord.check_payload_filename_duplicate(ast):
        return [token]
    
    token.value = ast.get_legal_value()
    # Check if current path exist.
    PathRecord.check_payload_path_exist(ast)

    return [token]
