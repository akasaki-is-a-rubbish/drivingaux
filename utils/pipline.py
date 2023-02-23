import collections

class pipline:
    def __init__(self, identifier:str):
        self.identifier = identifier
        def default_cnt()->int:
            return 0
        self.counter = collections.defaultdict(default_cnt)
        