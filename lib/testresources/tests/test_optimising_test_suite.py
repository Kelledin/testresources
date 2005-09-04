#
#  testresources: extensions to python unittest to allow declaritive use
#  of resources by test cases.
#  Copyright (C) 2005  Robert Collins <robertc@robertcollins.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import testresources
import testresources.tests
import unittest

def test_suite():
    loader = testresources.tests.TestUtil.TestLoader()
    result = loader.loadTestsFromName(__name__)
    return result
    

class TestOptimisingTestSuite(unittest.TestCase):

    def testImports(self):
        from testresources import OptimisingTestSuite

    def testAdsorbSuiteWithCase(self):
        suite = testresources.OptimisingTestSuite()
        case = unittest.TestCase("run")
        suite.adsorbSuite(case)
        self.assertEqual(len(suite._tests), 1)
        self.assertEqual(suite._tests[0], case)

    def testSingleCaseResourceAcquisition(self):
        class ResourceChecker(testresources.ResourcedTestCase):
            _resources = [("_default", testresources.SampleTestResource)]
            def getResourceCount(self):
                self.assertEqual(testresources.SampleTestResource._uses, 2)
                
        suite = testresources.OptimisingTestSuite()
        case = ResourceChecker("getResourceCount")
        suite.addTest(case)
        result = unittest.TestResult()
        suite.run(result)
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.failures, [])
        self.assertEqual(testresources.SampleTestResource._uses, 0)
        
        