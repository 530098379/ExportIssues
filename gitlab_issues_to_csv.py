import csv
import requests

auth = None
state = 'all'
repository = ''
private_token = ''

def write_issues(r, csvout):
    if r.status_code != 200:
        raise Exception(r.status_code)
    for issue in r.json():
        if 'pull_request' not in issue:
            comments = ''
            date = issue['created_at'].split('T')[0]
            if issue['user_notes_count'] > 0:
                url = '{}/{}/issues/{}/notes'.format(repository, project_id, issue['iid'])
                r2 = requests.get(url, headers = headers)
                for comment in r2.json():
                    comments += '\r\n' + comment['body']

            csvout.writerow([issue['title'], issue['description'] + comments, issue['iid']])

def get_issues():
    url = '{}/{}/issues'.format(repository, project_id)
    r = requests.get(url, headers = headers)

    csvfilename = 'project_id-{}-issues.csv'.format(project_id)
    with open(csvfilename, 'w', encoding='utf-8', newline='') as csvfile:
        csvout = csv.writer(csvfile)
        csvout.writerow(['Title', 'Description', 'iid'])

        write_issues(r, csvout)

        if 'link' in r.headers:
            pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                     (link.split(';') for link in
                      r.headers['link'].split(','))}
            while 'last' in pages and 'next' in pages:
                pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                         (link.split(';') for link in
                          r.headers['link'].split(','))}
                r = requests.get(pages['next'], headers = headers)
                write_issues(r, csvout)
                if pages['next'] == pages['last']:
                    break

if __name__ == '__main__':
    project_id = '3'
    repository = 'http://10.236.37.241:28080/api/v4/projects' #项目地址
    private_token = '在gitlab设置的token'
    headers = {'PRIVATE-TOKEN':private_token}
    get_issues()
