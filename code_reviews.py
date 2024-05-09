from statistics import mean
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from merge_request import MergeRequest

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
    """Gets the percentage of review checklist items ticked in total"""
    i = 1
    merge_request_forms = 0
    total_percentage = 0

    items_checked = []
    occurrences = {}
    for merge_request in merge_requests:
        checked = merge_request.number_checked()
        total_checks = len(merge_request.checklist)
        if total_checks > 0:
            percentage = checked / len(merge_request.checklist) * 100
            merge_request_forms += 1
            total_percentage += percentage
        else:
            percentage = None

        if percentage not in occurrences:
            occurrences[percentage] = 1
        else:
            occurrences[percentage] += 1

        print('{} - Items checked: {}/{} - {}%'.format(i, checked, total_checks, percentage))
        row = {'Items Checked': checked, 'Total Checks': total_checks, 'Percentage Coverage': percentage}
        items_checked.append(row)
        i += 1
    
    with open('coverage_occurrences.txt', 'w') as occ_file:
        occ_file.write('#checked/#items: #occurrences\n')
        for key, value in occurrences.items():
            occ_file.write('{}: {}\n'.format(key, value))

    fields = [key for key in items_checked[0]]
    write_results('review_coverage', items_checked, fields)
    average_checked = total_percentage/merge_request_forms
    print('Average percentage checked: {}, coverage recorded'.format(average_checked))

def record_notes(merge_requests):
    f = open('review_notes.txt', 'w')
    for merge_request in merge_requests:
        notes = merge_request.get_all_notes()
        for note in notes:
            lines = ['-----------------------------\n{}\n'.format(note.author), '{}\n'.format(note.created_at), '{}\n'.format(note.body), '-----------------------------\n']
            f.writelines(lines)
    f.close()
    print('Notes recorded')

def plot_discussion_density(merge_requests):
    """Plots the number of resolvable comments over the time of the project"""
    date_notes = {}
    for merge_request in merge_requests:
        notes = merge_request.get_all_notes()
        for note in notes:
            created_at = datetime.strptime(note.created_at[:10], '%Y-%m-%d')
            if created_at not in date_notes:
                date_notes[created_at] = 1
            else:
                date_notes[created_at] += 1
    dates_sorted = dict(sorted(date_notes.items()))
    dates = dates_sorted.keys()
    num_notes = dates_sorted.values()
    plt.title('Density of comments over time')
    plt.xlabel('Dates')
    plt.ylabel('Number of (resolvable) notes')
    plt.plot(dates, num_notes)
    plt.show()

def plot_discussion_distribution(merge_requests):
    """Plots the discussion distribution between the user. 
    It shows the total number of resolvable comments from each user"""
    author_notes = {}
    for merge_request in merge_requests:
        notes = merge_request.get_all_notes()
        for note in notes:
            author = note.author
            if author not in author_notes:
                author_notes[author] = 0
            else:
                author_notes[author] += 1
    print('Author discussion names: {}'.format(author_notes.keys()))
    authors = ['author{}'.format(i + 1) for i in range(len(author_notes.keys()))]
    num_notes = author_notes.values()
    plt.bar(authors, num_notes)
    plt.xlabel('Authors')
    plt.ylabel('Number of Notes')
    plt.title('Number of Notes Per User')
    plt.show()

def plot_note_length(merge_requests):
    """Plots the length of every note and the date that they were last updated"""
    note_lengths = []
    notes_last_updated = []
    for merge_request in merge_requests:
        notes = merge_request.get_all_notes()
        for note in notes:
            note_length = len(note.body)
            last_updated = datetime.strptime(note.updated_at[:10], '%Y-%m-%d')
            note_lengths.append(note_length)
            notes_last_updated.append(last_updated)
    plt.scatter(notes_last_updated, note_lengths)
    plt.title('Length of Comments over Time')
    plt.xlabel('Last Updated')
    plt.ylabel('Length of note')
    plt.show()

def plot_average_lengths(merge_requests):
    """Plots how long each developer makes their comments"""
    author_note_lengths = {}
    for merge_request in merge_requests:
        notes = merge_request.get_all_notes()
        for note in notes:
            author = note.author
            if author not in author_note_lengths:
                author_note_lengths[author] = []
            else:
                author_note_lengths[author].append(len(note.body))
    print('Author note lengths keys: {}'.format(author_note_lengths.keys()))
    print(author_note_lengths)
    authors = ['Author {}'.format(i + 1) for i in range(len(author_note_lengths.keys()))]
    average_lengths = [mean(note_lengths) for note_lengths in author_note_lengths.values()]
    plt.bar(authors, average_lengths)
    plt.xlabel('Authors')
    plt.ylabel('Average note lengths')
    plt.show()

def get_data(project):
    """
    - TODO length of notes over time
    - TODO length of notes per developer
    - TODO how they use sonarqube report in the review
    """
    merge_requests = get_merge_requests(project)
    review_forms = get_review_forms(merge_requests)

    for form in review_forms:
        for item in form:
            print(item)
        print('==========')

    get_review_coverage(merge_requests)
    record_notes(merge_requests)
    plot_discussion_density(merge_requests)
    plot_discussion_distribution(merge_requests)
    plot_note_length(merge_requests)
    plot_average_lengths(merge_requests)