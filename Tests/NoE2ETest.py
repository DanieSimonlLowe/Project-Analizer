from Merge import Merge
from Tests.MergeTest import MergeTest
from dateutil.parser import parse


class NoE2ETest(MergeTest):
    MIN_MERGE = parse('2023-05-22 08:40:19 UTC')

    def _run(self, merge: Merge):
        for change in merge.get_changes():

            if 'playwright' in change['diff']:
                self.fails.append(merge)
                return
        self.passes.append(merge)
