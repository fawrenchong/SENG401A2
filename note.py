class Note:
    def __init__(self, dict_obj):
        self.id = dict_obj['id']
        self.body = dict_obj['body']
        self.author = dict_obj['author']['username']