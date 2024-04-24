class CheckItem:
    def __init__(self, string):
        self.is_marked = string[1] == 'x'
        self.description = string[3:]