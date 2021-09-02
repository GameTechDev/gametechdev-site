import json
import requests
import sys
import yaml
from bs4 import BeautifulSoup
from os.path import exists
from os import mkdir, environ


def dump_json(output, data_to_save):
    save = open(output, 'w')
    json.dump(data_to_save, save)
    save.close()
    print('Saved json to', output)


def dump_yaml(output, data_to_save):
    save = open(output, 'w')
    yaml.dump(data_to_save, save)
    save.close()
    print('Saved yaml to', output)


if __name__ == '__main__':
    reposUrl = ''
    authToken = ''

    if len(sys.argv) > 1:
        reposUrl = sys.argv[1]
        authToken = sys.argv[2]
    else:
        # an orgs' repo list API url, in form of https://api.github.com/orgs/{org}/repos
        reposUrl = environ['GITHUB_CONTENT_SYNC_ORG_REPOS_URL']
        # an auth token for example a PAT
        authToken = environ['GITHUB_CONTENT_SYNC_PAT']

    # info to be pulled from github
    initDict = {
        'id': 0,
        'name': '',
        'description': '',
        'created_at': '',
        'updated_at': '',
        'pushed_at': '',
        'license': '',
        'html_url': '',
        'topics': [],
        'homepage': '',
        # we won't be getting the social img url from github's data source, but we need to instantiate it
        'social_img_url': ''
    }

    headerValues = {
        # We should explicitly access the latest api version per github api
        'default': 'application/vnd.github.v3+json',
        # To access topics, we must explicitly access a preview api version
        'topics': 'application/vnd.github.mercy-preview+json'
    }

    contentOutput = []
    repos = []
    topics = set(())

    keepIndexing = True

    print(f'Attempting to get content from {reposUrl}.')

    apiPage = 1
    while keepIndexing:
        requestParams = {'page': apiPage, 'sort': 'updated'}
        getRepos = requests.get(
            reposUrl,
            headers={
                'Accept': headerValues['topics'],
                'Authorization': f'token {authToken}'
            },
            params=requestParams
        )

        if getRepos.status_code != 200:
            keepIndexing = False
            print('Received non-200 status code', getRepos.status_code, 'while trying to scan repos. This generally '
                                                                        'means the process will fail. Likely you need '
                                                                        'to authenticate to get past Github API '
                                                                        'Limits. Halting content generation.')
            raise ValueError('Got non-200 status when trying to get content.')

        # Repo information syncing loop
        elif keepIndexing:
            if not json.loads(getRepos.text):
                keepIndexing = False
                print(f'End of list reached.')
            else:
                print(f'Saving page {apiPage} of API response and getting imagery URLs...')
                for repo in json.loads(getRepos.text):
                    if not repo['archived']:
                        for topic in repo['topics']:
                            topics.add(topic)

                        # Initialize an empty list entry
                        compileRepoInfo = initDict.copy()
                        # Iterate over data placeholders and pull the data from the correct repo in memory
                        for detail in compileRepoInfo:
                            if detail in repo:
                                compileRepoInfo[detail] = repo[detail]
                                if detail == 'html_url':
                                    pageContent = requests.get(repo[detail]).text
                                    parsePage = BeautifulSoup(pageContent, "html.parser")
                                    # limit tag search to head
                                    pageHead = parsePage.html.find('head')
                                    socialImageElement = pageHead.find("meta", attrs={"property": "og:image"})
                                    if socialImageElement:
                                        if socialImageElement.has_attr('content'):
                                            compileRepoInfo['social_img_url'] = socialImageElement['content']

                        # Add to list of compiled repo entries for final output
                        contentOutput.append(compileRepoInfo)
                apiPage += 1

    print('Collating content...')
    if not exists('../assets/img/thumb/'):
        mkdir('../assets/img/thumb/')

    sortedTopics = list(topics)
    sortedTopics.sort()
    dump_json('../_data/topics.json', sortedTopics)
    dump_json('../_data/projects.json', contentOutput)

    print('Downloading images...')
    for repo in contentOutput:
        response = requests.get(repo['social_img_url'])
        if response.ok:
            file_name = repo['name']
            file_type = response.headers['content-type'].split('/')[1]
            with open(f'../assets/img/thumb/{file_name}.{file_type}', 'wb') as file:
                file.write(response.content)
