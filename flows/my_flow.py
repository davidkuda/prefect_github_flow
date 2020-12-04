import api_client_register_flow
from prefect import task, Flow
from prefect.environments.storage import GitHub
from prefect.run_configs.local import LocalRun


@task()
def get_data():
    return [1, 2, 3, 4, 5]


@task()
def print_data(data):
    print(data)


storage = GitHub(
    repo="pnd-dkuda/prefect_github_flow",
    path="flows/my_flow.py",
    secrets=["GITHUB_ACCESS_TOKEN"]
)


run_config = LocalRun(
    env={'GITHUB_ACCESS_TOKEN': 'x',
         'PREFECT__CONTEXT__SECRETS__GITHUB_ACCESS_TOKEN': 'x'}
)


with Flow("file-based-flow",
          storage=storage,
          run_config=run_config
          ) as flow:
    data = get_data()
    print_data(data)


if __name__ == '__main__':

    api_client = api_client_register_flow.RegisterFlow(
        flow=flow,
        project_id='f6118a7e-81e9-46a7-9f2b-9da972825a06',
        api_base_url='https://localhost:4200'
    )

    api_client.register_flow()