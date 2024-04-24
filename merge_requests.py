from discussion import Discussion
from statistics import mean
from check_item import CheckItem 

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
        """Returns a list of all the notes in every discussion"""
        notes = []
        for discussion in self.discussions:
            for note in discussion.notes:
                if note.author != BOT_NAME:
                    notes.append(note)
        return notes

    def get_checklist_items(self):
        review_form_string = '## Review Form'
        if review_form_string not in self.description:
            return []
        else:
            checklist_string = self.description.split(review_form_string)[-1].strip()
            checklist_items = checklist_string.split('\n- ')
            checklist_items[0] = checklist_items[0][2:]
            return [CheckItem(checklist_item) for checklist_item in checklist_items]

def get_average_discussions(merge_requests):
    """This does not count the comment automatically made by SonarQube"""
    note_counts = [len(merge_request.get_all_notes()) for merge_request in merge_requests]
    return mean(note_counts)

def get_merge_requests(project):
    project_merge_requests = project.mergerequests.list(get_all=False)
    merge_requests = [MergeRequest(project_merge_request) for project_merge_request in project_merge_requests]

    mr = merge_requests[0]
    for check_item in mr.checklist:
        print(check_item.is_marked, check_item.description)
    