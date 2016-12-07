#!/usr/bin/env python
"""
.. py:currentmodule:: test_analysis
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module `analysis`.
"""

###############################################################################
# Copyright 2016 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# Standard library modules.
import unittest
import os.path

# Third party modules.

# Local modules.
import pyHendrixDemersTools.Files as Files

# Project modules
from pyxrayphasemap.analysis import PhaseAnalysis

# Globals and constants variables.


class Testanalysis(unittest.TestCase):
    """
    TestCase class for the module `analysis`.
    """

    def setUp(self):
        """
        Setup method.
        """

        unittest.TestCase.setUp(self)

        self.test_data_path = Files.getCurrentModulePath(__file__, "../test_data")

    def tearDown(self):
        """
        Teardown method.
        """

        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        """
        First test to check if the testcase is working with the testing framework.
        """

        # self.fail("Test if the testcase is working.")

    def test_test_data_path(self):
        """
        Tests for method :py:meth:`test_data_path`.
        """

        test_data_path = Files.getCurrentModulePath(__file__, "../test_data")

        self.assertTrue(os.path.isdir(test_data_path))

    def test__readDataFromTextFile(self):
        """
        Tests for method :py:meth:`_readDataFromTextFile`.
        """

        phase_analysis = PhaseAnalysis("Dummy_file_path")
        file_path = os.path.join(self.test_data_path, "bruker", "good_text_export.txt")
        data = phase_analysis._readDataFromTextFile(file_path)

        print(data.shape)
#        self.fail("Test if the testcase is working.")

if __name__ == '__main__':  # pragma: no cover
    import nose
    import sys
    argv = sys.argv
    argv.append("--cover-package=pyxrayphasemap.analysis")
    nose.runmodule(argv=argv)
