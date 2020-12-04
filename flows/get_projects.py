import requests
from prefect import task, Flow, config, context
from prefect.environments.storage import GitHub
import os


# --- Env Vars --- #
# os.environ['KEY'] = 'VALUE'


# BASE_URL = 'https://agent.prefect.docs.pandata.de/'
BASE_URL = 'http://localhost:4202/'
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


@task()
def say_hello():
    print("Hello, world!")

@task()
def get_data():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9]

@task()
def get_data_bravo():
    return ['a', 'b', 'c']

@task()
def print_data(data):
    print(data)

@task()
def print_env():
    print(os.environ)


@task()
def get_projects():
    r = requests.post(BASE_URL, json={'query': query}, headers=headers).json()
    return r


# --- Set Schedule // simple --- #
from datetime import time, timedelta
from prefect.schedules import IntervalSchedule
schedule = IntervalSchedule(interval=timedelta(minutes=30))


# --- Set Schedule // complex --- #
# from datetime import time, timedelta
# from prefect.schedules import Schedule, filters
# from prefect.schedules.clocks import IntervalClock
# from prefect.schedules import IntervalSchedule
#
#
# schedule = Schedule(
#     # emit an event every hour
#     clocks=[IntervalClock(interval=timedelta(hours=1))],
#
#     # only include weekdays
#     filters=[filters.is_weekday],
#
#     # only include 9am and 5pm
#     or_filters=[
#         filters.between_times(time(9), time(9)),
#         filters.between_times(time(17), time(17))
#     ]
# )
#
schedule.next(4)


# --- Register the flow --- #

with Flow(
        "experiment_flow",
        schedule=schedule,
        storage=GitHub(
            repo="pnd-dkuda/prefect_github_flow",
            path="flows/get_projects.py",
            secrets=["GITHUB_ACCESS_TOKEN"]
        )) as flow:
    say_hello()
    data = get_data()
    data_bravo = get_data_bravo()
    print_data(data)
    print_env()


# --- Set flow storage to GitHub --- #

# flow.storage = GitHub(
#     repo="pnd-dkuda/prefect_github_flow",
#     path="flows/get_projects.py",
#     secrets=["GITHUB_ACCESS_TOKEN"]
# )


# --- Register flow to prefect --- #

flow_bytes = flow.serialize()

variables = {
  "projectId": "f6118a7e-81e9-46a7-9f2b-9da972825a06",
  "flow": flow_bytes
}

if __name__ == '__main__':
    # r = requests.post(BASE_URL, json={'query': query}, headers=headers).json()
    # print(r)

    if 'HOME' in os.environ:
        print('HOME environment variable is already defined. Value =', os.environ['HOME'])
    else:
        print('HOME environment variable is not defined.')

    print(os.environ)

    post = requests.post(BASE_URL, json={'query': mutation_flow, 'variables': variables}, headers=headers).json()
    print(post)
