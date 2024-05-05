import pandas

from Merge import Merge
from Tests.AllTestsTest import AllTestsTest
from Tests.BranchNameTest import BranchNameTest
from Tests.CoverageTest import CoverageTest
from tqdm import tqdm

from Tests.DevMergeTest import DevMergeTest
from Tests.NoE2ETest import NoE2ETest
from Tests.SmellTest import SmellTest
from Tests.SonarQubeTest import SonarQubeTest
from noReqeast import get_no_request_merges

csv = pandas.read_csv('seng302-2023-team-1000_merge_requests.csv')

allTest = AllTestsTest()
nameTest = BranchNameTest()
coverageTest = CoverageTest()
devTest = DevMergeTest()
noE2ETest = NoE2ETest()
smellTest = SmellTest()
sqTest = SonarQubeTest()

tests = [allTest, nameTest, coverageTest, devTest, noE2ETest, smellTest, sqTest]

merges = []
for i, line in tqdm(list(csv.iterrows())):
    m = Merge(line)
    for test in tests:
        test.test(m)

allTest.output('allTest_fail', 'allTest_success')
nameTest.output('nameTest_fail', 'nameTest_success')
coverageTest.output('coverageTest_fail', 'coverageTest_success')
devTest.output('devTest_fail', 'devTest_success')
noE2ETest.output('noE2ETest_fail', 'noE2ETest_success')
smellTest.output('smellTest_fail', 'smellTest_success')
sqTest.output('sqTest_fail', 'sqTest_success')

# test.output('e2e_fails', 'e2e_passes')
