import requests
from prefect import task, Flow
from prefect.environments.storage import GitHub


BASE_URL = 'https://agent.prefect.docs.pandata.de/'
query = 'query {project {id name}}'
headers = {'Accept-Encoding': 'gzip, deflate, br',
           'Content-Type': 'application/json',
           'Accept': 'application/json',
           'Connection': 'keep-alive',
           'DNT': '1',
           'Origin': 'https://agent.prefect.docs.pandata.de'}

mutation_flow = '''
mutation register_flow($flow: JSON!, $projectId: UUID!) {
  create_flow(input: { serialized_flow: $flow, project_id: $projectId }) {
    id
  }
}
'''


@task
def get_data():
    return [1, 2, 3, 4, 5]

@task
def print_data(data):
    print(data)

@task
def get_projects():
    r = requests.post(BASE_URL, json={'query': query}, headers=headers).json()
    return r


with Flow("file-based-flow") as flow:
    data = get_data()
    print_data(data)
    projects = get_projects()
    print_data(projects)

flow.storage = GitHub(
    repo="pnd-dkuda/prefect_github_flow",
    path="get_projects.py",
    # secrets=["GITHUB_ACCESS_TOKEN"]
)

flow_bytes = flow.serialize()
variables = {
  "projectId": "f6118a7e-81e9-46a7-9f2b-9da972825a06",
  "flow": flow_bytes
}

if __name__ == '__main__':
    # r = requests.post(BASE_URL, json={'query': query}, headers=headers).json()
    # print(r)

    post = requests.post(BASE_URL, json={'query': mutation_flow, 'variables': variables}, headers=headers).json()
    print(post)
