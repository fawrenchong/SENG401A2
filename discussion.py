class Discussion:
    def __init__(self, gitlab_obj):
        self.gitlab_obj = gitlab_obj
        self.id = gitlab_obj.id
        self.individual_note = gitlab_obj.individual_note
        self.notes = gitlab_obj.attributes['notes']