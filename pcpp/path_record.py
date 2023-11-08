



global CURRENT_FILE
CURRENT_FILE = "/"


class PathRecord(object):

    CURRENT_FILE = "/"

    INCLUDE_PATH_LIST = []
    PAYLOAD_PATH_LIST = []

    @classmethod
    def check_include_path_duplicate(cls,token):

        dup = False
        for e in cls.INCLUDE_PATH_LIST:
            if token.value == e.value:
                print(f'[INFO] Include Path {token.value} in {token.file}:{token.lineno} is duplicated with {e.file}:{e.lineno} and is therefore ignored.')
                dup = True
        return dup
    
    @classmethod
    def check_payload_path_duplicate(cls,token):

        dup = False
        for e in cls.PAYLOAD_PATH_LIST:
            if token.value == e.value:
                print(f'[INFO] Path {token.value} in {token.file}:{token.lineno} is duplicated with {e.file}:{e.lineno} and is therefore ignored.')
                dup = True
        return dup