import requests


class RegisterFlow:

    def __init__(self, flow, project_id, api_base_url):
        self.flow_bytes = flow.serialize()
        self.project_id = project_id
        self.base_url = api_base_url
        self.headers = {'Accept-Encoding': 'gzip, deflate, br',
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'Connection': 'keep-alive',
                        'DNT': '1',
                        'Origin': api_base_url}
        self.variables = {"flow": self.flow_bytes, "projectId": self.project_id}

    MUTATION_REGISTER_FLOW = '''
    mutation register_flow($flow: JSON!, $projectId: UUID!) {
      create_flow(input: { serialized_flow: $flow, project_id: $projectId }) {
        id
      }
    }
    '''

    def register_flow(self):
        r = requests.post(
            self.base_url,
            json={
                'query': self.MUTATION_REGISTER_FLOW,
                'variables': self.variables},
            headers=self.headers
        ).json()
