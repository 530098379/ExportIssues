"""
Exports issues from a list of repositories to individual csv files.
Uses basic authentication (Github username + password) to retrieve issues
from a repository that username has access to. Supports Github API v3.
Forked from: unbracketed/export_repo_issues_to_csv.py
"""
#import argparse
import csv
import requests
#from getpass import getpass


auth = None
state = 'all'
repository = ''


def write_issues(r, csvout):
    """Parses JSON response and writes to CSV."""
    if r.status_code != 200:
        raise Exception(r.status_code)
    for issue in r.json():
        if 'pull_request' not in issue:
            comments = ''
            labels = ', '.join([l['name'] for l in issue['labels']])
            date = issue['created_at'].split('T')[0]
            if issue['comments'] > 0:
                url = 'https://github.com/api/v3/repos/{}/issues/{}/comments'.format(repository, issue['number'])
                r2 = requests.get(url, auth=auth)
                for comment in r2.json():
                    comments += '\r\n' + comment['body']

            # Change the following line to write out additional fields
            csvout.writerow([issue['title'], issue['body'] + comments, issue['number']])
            """
            csvout.writerow([issue['number'], issue['url'], issue['title'], issue['state'], date, issue['body'],
                             'Author', 'Author Username', issue['assignee'], assignees,
                             'No', issue['locked'], date, issue['created_at'], issue['updated_at'],
                             issue['milestone'], '', labels, '', ''])
            """


def get_issues(name):
    """Requests issues from GitHub API and writes to CSV file."""
    url = 'https://github.com/api/v3/repos/{}/issues?state={}'.format(name, state)
    r = requests.get(url, auth=auth)

    csvfilename = '{}-issues.csv'.format(name.replace('/', '-'))
    with open(csvfilename, 'w', encoding='utf-8', newline='') as csvfile:
        csvout = csv.writer(csvfile)
        csvout.writerow(['Title', 'Description', 'number'])
        """
        csvout.writerow(['Issue ID', 'URL', 'Title', 'State', 'Description', 'Author',
                         'Author Username', 'Assignee', 'Assignee Username', 'Confidential',
                         'Locked', 'Due Date', 'Created At (UTC)', 'Updated At (UTC)',
                         'Milestone', 'Weight', 'Labels', 'Time Estimate', "Time Spen"])
        """
        write_issues(r, csvout)

        # Multiple requests are required if response is paged
        if 'link' in r.headers:
            pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                     (link.split(';') for link in
                      r.headers['link'].split(','))}
            while 'last' in pages and 'next' in pages:
                pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                         (link.split(';') for link in
                          r.headers['link'].split(','))}
                r = requests.get(pages['next'], auth=auth)
                write_issues(r, csvout)
                if pages['next'] == pages['last']:
                    break


"""
parser = argparse.ArgumentParser(description="Write GitHub repository issues "
                                             "to CSV file.")
parser.add_argument('repositories', nargs='+', help="Repository names, "
                    "formatted as 'username/repo'")
parser.add_argument('--all', action='store_true', help="Returns both open "
                    "and closed issues.")
args = parser.parse_args()

if args.all:
    state = 'all'

username = input("Username for 'https://github.com': ")
password = getpass("Password for 'https://{}@github.com': ".format(username))
"""
"""
username = '你的github邮箱'
password = '你的Personal access tokens'
repository = '组织名/项目名'
auth = (username, password)
#for repository in args.repositories:
get_issues(repository)
"""
if __name__ == '__main__':
    username = '你的github邮箱'
    password = '你的Personal access tokens'
    repository = '组织名/项目名'
    auth = (username, password)
    get_issues(repository)
