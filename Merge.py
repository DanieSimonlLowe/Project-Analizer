import os
import subprocess

import requests

from constants import BASE_URL, PROJECT_ID, TOKEN
from dateutil.parser import parse


def commit_hash_to_date(commit_hash):
    os.chdir('/csse/users/dlo54/Desktop/seng401/ass2/team-1000')
    process = subprocess.Popen(['git', 'show', '--no-patch', '--format=%ci', commit_hash],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = process.communicate()
    out = out.strip()
    return out


class Merge:
    def __init__(self, line):
        self.line = line
        self._commits = None
        self._merge = None
        self._last_dev = None
        self._pipline = None

    def get_is_merged(self):
        return self.line['State'] == 'merged'

    # def get_merge_date(self):
    #     return parse(self.get_commit()['created_at'])

    def get_commit(self):
        if self._commits is not None:
            # print('merge commit', self._commits[0]['short_id'])
            return self._commits[0]

        url = BASE_URL + 'projects/' + PROJECT_ID + '/merge_requests/' + str(self.line['MR IID']) + '/commits'

        self._commits = requests.get(
            url=url,
            params={'access_token': TOKEN}
        ).json()
        if len(self._commits) == 0:
            self._commits = [{'short_id': '0'}]

        return self._commits[0]

    def get_changes(self):
        if self._merge is not None:
            return self._merge['changes']

        url = BASE_URL + 'projects/' + PROJECT_ID + '/merge_requests/' + str(self.line['MR IID']) + '/changes'
        self._merge = requests.get(
            url=url,
            params={'access_token': TOKEN}
        ).json()

        return self._merge['changes']

    def get_merge_date(self):
        if self._merge is not None:
            return parse(self._merge['merged_at'])
        self.get_changes()

        return parse(self._merge['merged_at'])

    def get_last_dev(self):
        if self._last_dev is not None:
            return self._last_dev

        date = self.get_merge_date()
        before = '--before={y}-{m}-{d}'.format(y=date.year, m=date.month, d=date.day)
        os.chdir('/csse/users/dlo54/Desktop/seng401/ass2/team-1000')
        process = subprocess.Popen(['git', 'log', before, '-n', '1', '--pretty=format:"%H"'],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        self._last_dev = str(out.rstrip())[3:-2]
        return self._last_dev

    def get_pipeline(self):
        if self._pipline is not None:
            return self._pipline

        url = BASE_URL + 'projects/' + PROJECT_ID + '/merge_requests/' + str(self.line['MR IID']) + '/pipelines'

        pipelineJson = requests.get(
            url=url,
            params={'access_token': TOKEN}
        ).json()

        pipe_id = pipelineJson[0]['id']

        self._pipline = requests.get(
            url=BASE_URL + 'projects/' + PROJECT_ID + '/pipelines/' + str(pipe_id),
            params={'access_token': TOKEN}
        ).json()

        return self._pipline
