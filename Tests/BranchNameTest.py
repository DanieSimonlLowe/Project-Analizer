from Merge import Merge
from Tests.MergeTest import MergeTest
import re
from dateutil.parser import parse


class BranchNameTest(MergeTest):
    MIN_MERGE = parse('2023-04-6 08:40:19 UTC')

    def _run(self, merge: Merge):
        branch_name: str = merge.line['Source Branch']
        branch_name = branch_name.lower()
        if branch_name == 'dev' or branch_name == 'main':
            self.passes.append(merge)

        if re.match("^u[0-9]+(_[a-z]+)+$", branch_name):
            self.passes.append(merge)
        else:
            self.fails.append(merge)
