import unittest
from test.FileGrabberModule_test import FileGrabberTestMain
from FileGrabber import FileGrabber
from FileGrabber.InfoClass import Websites


# Todo: belows
class _FileGrabberTest(FileGrabberTestMain):
    @classmethod
    def setUpClass(cls):
        pass

    def test_grab_files(self):
        self.fail()

    def test_create_module(self):
        with self.assertRaises(ValueError):
            FileGrabber.create_module(None)
                
        webs = (Websites.CLIEN, Websites.THEQOO)
        for web in webs:
            result = FileGrabber.create_module(web)
            if web == Websites.CLIEN:
                from FileGrabber.Module import Clien
                self.assertIsInstance(result, Clien)
            elif web == Websites.THEQOO:
                from FileGrabber.Module import Theqoo
                self.assertIsInstance(result, Theqoo)


if __name__ == '__main__':
    unittest.main()
