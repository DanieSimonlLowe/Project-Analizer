import requests
from requests.auth import HTTPBasicAuth

from Merge import Merge, commit_hash_to_date
from Tests.MergeTest import MergeTest
from dateutil.parser import parse

from constants import SONARQUBE_URL, SONARQUBE_USERNAME, SONARQUBE_PASSWORD, BASE_URL, PROJECT_ID, TOKEN


class CoverageTest(MergeTest):
    MIN_MERGE = parse('2023-05-22 08:40:19 UTC')
    MAX_MERGE = parse('2023-09-15 08:40:19 UTC')
    # new_coverage
    def _run(self, merge: Merge):

        response = requests.get(SONARQUBE_URL + 'measures/component',
                      params={
                          'component': 'team-1000',
                          'branch': merge.line['Source Branch'],
                          'metricKeys': 'new_coverage'
                      },
                      auth=HTTPBasicAuth(username=SONARQUBE_USERNAME, password=SONARQUBE_PASSWORD)).json()
        if 'errors' in response:
            return;

        measures = response['component']['measures']
        if len(measures) == 0:
            return

        value = float(measures[0]['period']['value'])
        if value < 80:
            self.fails.append(merge)
        else:
            self.passes.append(merge)
