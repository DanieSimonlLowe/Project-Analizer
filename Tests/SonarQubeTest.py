import requests
from requests.auth import HTTPBasicAuth

from Merge import Merge, commit_hash_to_date
from Tests.MergeTest import MergeTest
from dateutil.parser import parse

from constants import SONARQUBE_URL, SONARQUBE_USERNAME, SONARQUBE_PASSWORD, BASE_URL, PROJECT_ID, TOKEN


class SonarQubeTest(MergeTest):
    MIN_MERGE = parse('2023-07-20 08:40:19 UTC')

    # new_coverage
    def _run(self, merge: Merge):
        response = requests.get(SONARQUBE_URL + 'qualitygates/project_status',
                                params={
                                    'projectKey': 'team-1000',
                                    'branch': merge.line['Source Branch'],
                                },
                                auth=HTTPBasicAuth(username=SONARQUBE_USERNAME, password=SONARQUBE_PASSWORD)).json()

        if 'errors' in response:
            return

        if response['projectStatus']['status'] == 'OK':
            self.passes.append(merge)
        else:
            self.fails.append(merge)

