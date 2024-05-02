from discussion import Discussion
from statistics import mean
from check_item import CheckItem 
import csv

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

def get_average_discussions(merge_requests):
    """This does not count the comment automatically made by SonarQube"""
    note_counts = [len(merge_request.get_all_notes()) for merge_request in merge_requests]
    return mean(note_counts)

def get_merge_requests(project):
    project_merge_requests = project.mergerequests.list(get_all=True)
    merge_requests = [MergeRequest(project_merge_request) for project_merge_request in project_merge_requests]
    return merge_requests

def get_review_forms(merge_requests):
    review_forms = {}

    for merge_request in merge_requests:
        check_items = tuple([check_item.description for check_item in merge_request.checklist])
        if check_items not in review_forms:
            review_forms[check_items] = [merge_request]
        else:
            review_forms[check_items].append(merge_request)

    return review_forms

def write_results(name, results, fields):
    with open('{}.csv'.format(name), 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

def get_review_coverage(merge_requests):
    i = 1
    merge_request_forms = 0
    total_percentage = 0

    items_checked = []
    for merge_request in merge_requests:
        checked = merge_request.number_checked()
        if len(merge_request.checklist) > 0:
            percentage = checked / len(merge_request.checklist) * 100
            merge_request_forms += 1
            total_percentage += percentage
        else:
            percentage = None
        print('{} - Items checked: {}/{} - {}%'.format(i, checked, len(merge_request.checklist), percentage))
        row = {'Items Checked': checked, 'Total Checks': len(merge_request.checklist), 'Percentage Coverage': percentage}
        items_checked.append(row)
        i += 1
    
    fields = [key for key in items_checked[0]]
    write_results('review_coverage', items_checked, fields)
    average_checked = total_percentage/merge_request_forms
    print('Average percentage checked: {}'.format(average_checked))

def record_notes(merge_requests):
    f = open('review_notes.txt', 'w')
    for merge_request in merge_requests:
        notes = merge_request.get_all_notes()
        for note in notes:
            lines = ['-----------------------------\n{}\n'.format(note.author), '{}\n'.format(note.created_at), '{}\n'.format(note.body), '-----------------------------\n']
            f.writelines(lines)
    f.close()

def get_data(project):
    merge_requests = get_merge_requests(project)
    review_forms = get_review_forms(merge_requests)

    # for form in review_forms:
    #     for item in form:
    #         print(item)
    #     print('==========')

    # get_review_coverage(merge_requests)

    record_notes(merge_requests)