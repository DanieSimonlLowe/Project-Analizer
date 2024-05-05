import os
import subprocess

from Merge import Merge
from Tests.MergeTest import MergeTest
from dateutil.parser import parse


class AllTestsTest(MergeTest):
    MIN_MERGE = parse('2023-04-6 08:40:19 UTC')

    def _run(self, merge: Merge):
        commit = merge.get_commit()

        os.chdir('/csse/users/dlo54/Desktop/seng401/ass2/team-1000')
        os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-1.17.0-openjdk-amd64'
        subprocess.run(['git', 'checkout', '-f', commit['short_id']])

        process = subprocess.Popen(['./gradlew', 'test'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        out = out.rstrip()
        if 'SUCCESSFUL' in str(out) or len(err) > 0:
            self.passes.append(merge)
        else:
            self.fails.append(merge)
