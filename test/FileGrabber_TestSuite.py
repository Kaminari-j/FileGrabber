import unittest

import FileGrabber_test
import FileGrabberModule_test
import InfoClass_test


def testSuite():
    suite = unittest.TestSuite()

    suite.addTest(InfoClass_test.TestWebservices('test_get_webservices_dict'))

    suite.addTest(FileGrabberModule_test.test_Common('test_getBsobj'))
    suite.addTest(FileGrabberModule_test.test_Common('test_file_download'))
    suite.addTest(FileGrabberModule_test.test_Common('test_verify_website'))

    suite.addTest(FileGrabberModule_test.test_Clien('test_get_article'))
    suite.addTest(FileGrabberModule_test.test_Clien('test_collect_files_from_article'))

    suite.addTest(FileGrabberModule_test.test_Theqoo('test_get_article'))
    suite.addTest(FileGrabberModule_test.test_Theqoo('test_get_article'))
    suite.addTest(FileGrabberModule_test.test_Theqoo('test_collect_files_from_article'))
    suite.addTest(FileGrabberModule_test.test_Theqoo('test_convert_gfycat'))

    suite.addTest(FileGrabberModule_test.test_Instagram('test_reformat_url'))
    suite.addTest(FileGrabberModule_test.test_Instagram('test_get_article'))
    suite.addTest(FileGrabberModule_test.test_Instagram('test_collect_files_from_article'))

    suite.addTest(FileGrabber_test.FileGrabberTest('test_grab_files'))
    suite.addTest(FileGrabber_test.FileGrabberTest('test_create_module'))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = testSuite()
    runner.run(test_suite)
