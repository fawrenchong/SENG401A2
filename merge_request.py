from check_item import CheckItem 
from discussion import Discussion

BOT_NAME = 'group_18664_bot_ed7a929f2e2e383a315369833ef98d6b'

class MergeRequest:
    def __init__(self, gitlab_obj):
        self.gitlab_obj = gitlab_obj
        self.description = gitlab_obj.description
        self.author = gitlab_obj.author['username']
        self.discussions = [Discussion(dis) for dis in gitlab_obj.discussions.list(get_all=True)]
        self.checklist = self.get_checklist_items()

    def print_discussions(self):
        for discussion in self.discussions:
            discussion.gitlab_obj.pprint()

    def count_notes(self):
        return sum(len(discussion.notes) for discussion in self.discussions)
    
    def get_all_notes(self):
        """Returns a list of all the notes in every discussion
        gets only the notes that are resolvable"""
        notes = []
        for discussion in self.discussions:
            for note in discussion.notes:
                if note.author != BOT_NAME and note.resolvable:
                    notes.append(note)
        return notes

    def get_checklist_items(self):
        review_form_string = '## Review Form'
        if review_form_string not in self.description:
            return []
        else:
            checklist_string = self.description.split(review_form_string)[-1].strip()
            checklist_items = checklist_string.split('\n{} '.format(checklist_string[0]))
            checklist_items[0] = checklist_items[0][2:]
            return [CheckItem(checklist_item) for checklist_item in checklist_items]

    def number_checked(self):
        """Gets how many checklist items are marked"""
        checked = 0
        for item in self.checklist:
            if item.is_marked:
                checked += 1
        return checked