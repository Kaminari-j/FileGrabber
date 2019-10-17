import unittest


def suite():
    ts = unittest.TestSuite()

    ts.addTest(InfoClass_test.TestWebservices('test_get_webservices_dict'))

    ts.addTest(FileGrabberModule_test.test_Common('test_getBsobj'))
    ts.addTest(FileGrabberModule_test.test_Common('test_file_download'))
    ts.addTest(FileGrabberModule_test.test_Common('test_verify_website'))

    ts.addTest(FileGrabberModule_test.test_Clien('test_get_article'))
    ts.addTest(FileGrabberModule_test.test_Clien('test_collect_files_from_article'))

    ts.addTest(FileGrabberModule_test.test_Theqoo('test_get_article'))
    ts.addTest(FileGrabberModule_test.test_Theqoo('test_get_article'))
    ts.addTest(FileGrabberModule_test.test_Theqoo('test_collect_files_from_article'))
    ts.addTest(FileGrabberModule_test.test_Theqoo('test_convert_gfycat'))

    ts.addTest(FileGrabberModule_test.test_Instagram('test_reformat_url'))
    ts.addTest(FileGrabberModule_test.test_Instagram('test_get_article'))
    ts.addTest(FileGrabberModule_test.test_Instagram('test_collect_files_from_article'))

    ts.addTest(FileGrabber_test.FileGrabberTest('test_grab_files'))
    ts.addTest(FileGrabber_test.FileGrabberTest('test_create_module'))

    return ts


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)
