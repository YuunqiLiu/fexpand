

import os

import filecmp





global CURRENT_FILE
CURRENT_FILE = "/"


class PathRecord(object):

    CURRENT_FILE = "/"

    INCLUDE_PATH_LIST = []
    PAYLOAD_PATH_LIST = []
    PAYLOAD_FILENAME_LIST = []


    @classmethod
    def check_include_path_duplicate(cls,token):

        dup = False
        for e in cls.INCLUDE_PATH_LIST:
            if os.path.abspath(token.value) == os.path.abspath(e.value):
                val = token.value.replace('\n','')
                print(f'[Info] Ignore include {val} in {token.file}:{token.lineno} because it is duplicated with {e.value} in {e.file}:{e.lineno}.')
                dup = True
        return dup
    



    @classmethod
    def check_payload_path_duplicate(cls, node):

        if node.value is "":
            return False

        dup = False
        for e in cls.PAYLOAD_PATH_LIST:
           # print(e.value)
            if node.get_formatted_value() == e.get_formatted_value():
                val = node.value.replace('\n','')
                print(f'[INFO] Ignore path \"{val}\" in {node.file}:{node.lineno} because it is duplicated with {e.file}:{e.lineno}.')
                dup = True

        return dup
    
    @classmethod
    def check_payload_filename_duplicate(cls, node):
        if node.value is "":
            return True
        
        new_path, new_name = os.path.split(node.value)

        dup = False
        for e in cls.PAYLOAD_FILENAME_LIST:
            old_path, old_name = os.path.split(e.value)
            if new_name == old_name:
                dup = True
                conflict = not filecmp.cmp(node.value, e.value)

                if conflict:
                    print(f'[Error] Skip {node.value} in {node.file}:{node.lineno} because it has diff content with {e.value} in {e.file}:{e.lineno}.')
                else:
                    print(f'[Warning] Skip {node.value} in {node.file}:{node.lineno} because it has same content with {e.value} in {e.file}:{e.lineno}.')

        return dup

    # @classmethod
    # def check_file_conflict(cls, new_path):

    #     new_dir, new_name = os.path.split(new_path)

    #     for old_path in cls.PAYLOAD_PATH_LIST:
    #         old_dir, old_name = os.path.split(old_path)
    #         if new_name == old_name:
    #             conflict = not filecmp.cmp(new_path, old_path)

    #             if conflict:
    #                 print('[Conflict]')
    #             else:
    #                 print('[Warning] ')
    #             
    #             
    #     pass