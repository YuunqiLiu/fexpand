

import os
import filecmp
from prettytable import PrettyTable



global CURRENT_FILE
CURRENT_FILE = "/"

class GlobalRecorder(object):

    def __init__():
        pass

    def record_include_path_duplicate():
        pass

    def record_include_path_not_exist():
        pass

    def record_include_path_same_file_name():
        pass

    def record_payload_path_duplicate():
        pass

    def record_payload_path_not_exist():
        pass

    def record_payload_path_same_file_name():
        pass



class InfoList(object):

    INFO_LIST = []
    SEVERITY  = {
        "ICLD" : "Info"     ,
        "IPNE" : "Error"    ,
        "PPNE" : "Warning"  ,
        "IPD"  : "Info"     ,
        "PPD"  : "Info"     ,
        "PFDC" : "Error"    ,
        "PFSC" : "Warning"
    }

    SEVERITY_DESCRIPTION = {
        "ICLD" : "Normal -f Include"                                    ,
        "IPNE" : "Include Path Not Exist"                               ,
        "PPNE" : "Payload Path Not Exist"                               ,
        "IPD"  : "Include Path Duiplicate"                              ,
        "PPD"  : "Payload Path Duiplicate"                              ,
        "PFDC" : "Payload Filename conflict and have Different Content" ,
        "PFSC" : "Payload Filename conflict and have Same Content"
    }

    @classmethod
    def print(cls):
        table = PrettyTable()
        table.field_names = ["Code", "Num", "Severity", "Description"]
        
        for key in cls.SEVERITY.keys():
            info_list = [x for x in cls.INFO_LIST if x.code == key]

            table.add_row([key, len(info_list), cls.SEVERITY[key], cls.SEVERITY_DESCRIPTION[key]])
            #print(key, '  ', len(info_list))
        print(table)

class Information(object):

    @property
    def SEVERITY(self):
        return InfoList.SEVERITY 


    def __init__(self, code, string) -> None:
        self.code   = code
        self.string = string
        InfoList.INFO_LIST.append(self)
        #print(INFO_LIST)

    def format_log(self):
        return "[%s-%s] %s." % (self.SEVERITY[self.code], self.code, self.string)



class PathRecord(object):

    CURRENT_FILE = "/"

    INCLUDE_PATH_LIST = []
    PAYLOAD_PATH_LIST = []
    PAYLOAD_FILENAME_LIST = []


    @classmethod
    def include(cls, token):
        info = Information('ICLD', 'Include path \"{token.value}\" at {PathRecord.CURRENT_FILE}:{token.lineno}.')
        print(info.format_log())
        #print(f'[Info] Include path \"{token.value}\" at {PathRecord.CURRENT_FILE}:{token.lineno}.')

    @classmethod
    def check_include_path_exist(cls, token):
        if not os.path.exists(token.value):
            info = Information('IPNE', f'Skip include path {token.value} at {PathRecord.CURRENT_FILE}:{token.lineno} because it is not exist.')
            print(info.format_log())
            #print(f'[Error-IPNE] Skip include path {token.value} at {PathRecord.CURRENT_FILE}:{token.lineno} because it is not exist.')
            return False
        else:
            return True

    @classmethod
    def check_payload_path_exist(cls, token):
        if not os.path.exists(token.value):
            info = Information('PPNE', f'Payload path {token.value} at {PathRecord.CURRENT_FILE}:{token.lineno} is not exist.')
            print(info.format_log())
            #print(f'[Warning-PPNE] Payload path {token.value} at {PathRecord.CURRENT_FILE}:{token.lineno} is not exist.')
            return False
        else:
            return True


    @classmethod
    def check_include_path_duplicate(cls,token):

        dup = False
        for e in cls.INCLUDE_PATH_LIST:
            if os.path.abspath(token.value) == os.path.abspath(e.value):
                val = token.value.replace('\n','')
                info = Information('IPD', f'Ignore include {val} in {token.file}:{token.lineno} because it is duplicated with {e.value} in {e.file}:{e.lineno}.')
                print(info.format_log())
                #print(f'[Info-IPD] Ignore include {val} in {token.file}:{token.lineno} because it is duplicated with {e.value} in {e.file}:{e.lineno}.')
                dup = True
        return dup
    



    @classmethod
    def check_payload_path_duplicate(cls, node):

        if node.value == "":
            return False

        dup = False
        for e in cls.PAYLOAD_PATH_LIST:
            if node.get_formatted_value() == e.get_formatted_value():
                val = node.value.replace('\n','')

                info = Information('PPD', f'Ignore path \"{val}\" in {node.file}:{node.lineno} because it is duplicated with {e.file}:{e.lineno}.')
                print(info.format_log())
                #print(f'[INFO] Ignore path \"{val}\" in {node.file}:{node.lineno} because it is duplicated with {e.file}:{e.lineno}.')
                dup = True
        
        if not dup:
            cls.PAYLOAD_PATH_LIST.append(node)

        return dup
    
    @classmethod
    def check_payload_filename_duplicate(cls, node):
        if node.value == "":
            return True
        
        new_path, new_name = os.path.split(node.value)

        dup = False
        for e in cls.PAYLOAD_FILENAME_LIST:
            old_path, old_name = os.path.split(e.value)
            if new_name == old_name:
                dup = True
                conflict = not filecmp.cmp(node.value, e.value)

                if conflict:
                    info = Information('PFDC', f'Skip {node.value} in {node.file}:{node.lineno} because it has diff content with {e.value} in {e.file}:{e.lineno}.')
                    print(info.format_log())
                    #print(f'[Error] Skip {node.value} in {node.file}:{node.lineno} because it has diff content with {e.value} in {e.file}:{e.lineno}.')
                else:
                    info = Information('PFSC', f'Skip {node.value} in {node.file}:{node.lineno} because it has same content with {e.value} in {e.file}:{e.lineno}.')
                    print(info.format_log())
                    #print(f'[Warning] Skip {node.value} in {node.file}:{node.lineno} because it has same content with {e.value} in {e.file}:{e.lineno}.')
        
        if not dup:
            cls.PAYLOAD_FILENAME_LIST.append(node)


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