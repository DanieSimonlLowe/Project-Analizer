import os
import subprocess

from Merge import Merge
from Tests.MergeTest import MergeTest
from dateutil.parser import parse


class DevMergeTest(MergeTest):
    MIN_MERGE = parse('2023-05-24 08:40:19 UTC')

    def _run(self, merge: Merge):
        oid = merge.get_commit()['short_id']
        # date = merge.get_merge_date()
        # before = '--before={y}-{m}-{d}'.format(y=date.year, m=date.month, d=date.day)
        #
        # os.chdir('/csse/users/dlo54/Desktop/seng401/ass2/team-1000')
        # process = subprocess.Popen(['git', 'log', before, '-n', '1', '--pretty=format:"%H"'],
        #                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #
        # out, err = process.communicate()
        # last_dev = str(out.rstrip())[3:-2]

        process = subprocess.Popen(['git', 'merge-base', '--is-ancestor', merge.get_last_dev(), oid],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate()
        if process.returncode == 0:
            self.passes.append(merge)
        else:
            self.fails.append(merge)
