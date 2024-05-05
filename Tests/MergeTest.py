import os

import pandas as pd
from dateutil.parser import parse
import requests

from Merge import Merge


class MergeTest:
    MIN_MERGE = None
    MAX_MERGE = None

    def __init__(self):
        self.passes = []
        self.fails = []
        self.name = 'MergeTest'

    def _run(self, merge: Merge):
        pass

    def test(self, merge: Merge):
        if not merge.get_is_merged():
            return

        if self.MIN_MERGE is not None:
            merged_date = merge.get_merge_date()
            if merged_date < self.MIN_MERGE:
                return
        if self.MAX_MERGE is not None:
            merged_date = merge.get_merge_date()
            if merged_date > self.MAX_MERGE:
                return

        self._run(merge)

    def output(self, fail_name, pass_name):
        df_fail = pd.DataFrame(f.line.to_dict() for f in self.fails)
        df_pass = pd.DataFrame(p.line.to_dict() for p in self.passes)

        os.chdir('/csse/users/dlo54/Desktop/seng401/ass2')
        df_fail.to_csv(fail_name + '.csv', index=False)
        df_pass.to_csv(pass_name + '.csv', index=False)
