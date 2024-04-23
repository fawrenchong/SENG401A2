from discussion import Discussion

class MergeRequest:
    def __init__(self, gitlab_obj):
        self.gitlab_obj = gitlab_obj
        self.description = gitlab_obj.description
        self.author = gitlab_obj.author['username']
        self.discussions = [Discussion(dis) for dis in gitlab_obj.discussions.list(get_all=True)]

    def print_discussions(self):
        for discussion in self.discussions:
            discussion.pprint()

    def count_notes(self):
        return sum(len(discussion.notes) for discussion in self.discussions)
    
    def get_all_notes(self):
        """Returns a list of all the notes in every discussion"""
        notes = []
        for discussion in self.discussions:
            for note in discussion.notes:
                notes.append(note)
        return notes

def get_merge_requests(project):
    project_merge_requests = project.mergerequests.list(get_all=False)
    merge_requests = [MergeRequest(project_merge_request) for project_merge_request in project_merge_requests]

    mr = merge_requests[0]
    print(mr.author)