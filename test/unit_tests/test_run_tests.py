import os
import unittest
import tempfile
import shutil

import imp
imp.load_source('run_tests',
                os.path.join(os.path.dirname(__file__),
                             '..', '..', 'cmake', 'test', 'run_tests.py'))

from run_tests import main


class RunTestsTest(unittest.TestCase):

    def test_main(self):
        try:
            rootdir = tempfile.mkdtemp()
            results_file = os.path.join(rootdir, 'foo', 'testfile.xml')
            placeholder = os.path.join(rootdir, 'foo', 'MISSING-testfile.xml')
            # check_file = os.path.join(rootdir, 'checkfile')
            # with open(src_file, 'w') as fhand:
            #     fhand.write('foo')
            # self.assertTrue(os.path.isfile(check_file))
            main(['true',
                  results_file,
                  '--working-dir', rootdir])
            self.assertFalse(os.path.exists(results_file))
            self.assertTrue(os.path.exists(placeholder))
            with open(placeholder, 'r') as fhand:
                contents = fhand.read()
            self.assertTrue(results_file in contents)
            ###
            main(["echo '<testsuite></testsuite>' > %s" % results_file,
                  results_file,
                  '--working-dir', rootdir])
            self.assertTrue(os.path.exists(results_file))
            self.assertFalse(os.path.exists(placeholder))
            ### no working dir given
            main(["echo '<testsuite></testsuite>' > %s" % results_file,
                  results_file])
            self.assertTrue(os.path.exists(results_file))
            self.assertFalse(os.path.exists(placeholder))
            ### make sure resultsfile is deleted
            main(['true',
                  results_file,
                  '--working-dir', rootdir])
            self.assertFalse(os.path.exists(results_file))
            self.assertTrue(os.path.exists(placeholder))
            with open(placeholder, 'r') as fhand:
                contents = fhand.read()
            self.assertTrue(results_file in contents)
        finally:
            shutil.rmtree(rootdir)
