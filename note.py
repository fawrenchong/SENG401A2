class Note:
    def __init__(self, dict_obj):
        self.obj = dict_obj
        self.id = dict_obj['id']
        self.body = dict_obj['body']
        self.author = dict_obj['author']['username']
        self.resolvable = dict_obj['resolvable']
        self.created_at = dict_obj['created_at']
        self.updated_at = dict_obj['updated_at']