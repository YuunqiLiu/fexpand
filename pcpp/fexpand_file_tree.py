


CURRENT_FILE_NODE = '/'

class FileTreeNode(object):

    def __init__(self, status, path) -> None:
        self.path = path
        self.status = status
        self.son_list  = []

    
    def string(self, prefix=""):
        res = "%s[%s] %s\n" % (prefix, self.status, self.path)
        for s in self.son_list:
            res += s.string(prefix = " |-%s" % prefix)
        return res
    