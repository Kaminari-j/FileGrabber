import unittest
from test.FileGrabber_test import FileGrabberTestMain
from FileGrabber import main
from FileGrabber.InfoClass import Webservices


# Todo: belows
class MainTest(FileGrabberTestMain):
    @unittest.expectedFailure
    def download_file(self):
        self.fail()

    @unittest.expectedFailure
    def test_grab_files(self):
        self.fail()

    def test_create_module(self):
        from FileGrabber import FileGrabber
        with self.assertRaises(ValueError):
            main.create_module(None)
                
        urls = ('https://www.clien.net/service/board/park/13511316',
                'https://theqoo.net/1111082407',
                'https://www.instagram.com/p/Br84A_jFDVC')
        for url in urls:
            result = main.create_module(url)
            if url == Webservices.CLIEN:
                self.assertIsInstance(result, FileGrabber.Clien)
            elif url == Webservices.THEQOO:
                self.assertIsInstance(result, FileGrabber.Theqoo)
            elif url == Webservices.INSTAGRAM:
                self.assertIsInstance(result, FileGrabber.Instagram)


if __name__ == '__main__':
    unittest.main()
