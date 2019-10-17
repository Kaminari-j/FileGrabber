import unittest
from test.ForTest import FileGrabberTestMain
from FileGrabber import filegrabber
from FileGrabber.handler import grabbers
from FileGrabber.info import Webservices


# Todo: belows
class Test(FileGrabberTestMain):
    @unittest.expectedFailure
    def test_grab_files(self):
        self.fail()

    def test_verify_website(self):
        with self.assertRaises(ValueError):
            filegrabber.verify_website('https://www.naver.com')

        urls = {'clien': r'https://www.clien.net/service/board/park',
                'theqoo': r'https://theqoo.net/index.php?mid=square&filter_mode=normal&page=2&document_srl=1110055038'}
        for site, url in urls.items():
            result = filegrabber.verify_website(url)
            self.assertIsNotNone(result)
            if site == Webservices.CLIEN:
                self.assertEqual(result, Webservices.CLIEN)
            elif site == Webservices.THEQOO:
                self.assertEqual(result, Webservices.THEQOO)

    def test_create_module(self):
        with self.assertRaises(ValueError):
            filegrabber.create_module(None)
                
        urls = ('https://www.clien.net/service/board/park/13511316',
                'https://theqoo.net/1111082407',
                'https://www.instagram.com/p/Br84A_jFDVC')
        for url in urls:
            result = filegrabber.create_module(url)
            if url == Webservices.CLIEN:
                self.assertIsInstance(result, grabbers.Clien)
            elif url == Webservices.THEQOO:
                self.assertIsInstance(result, grabbers.Theqoo)
            elif url == Webservices.INSTAGRAM:
                self.assertIsInstance(result, grabbers.Instagram)

    # Todl: change method name to file_download_with_FileInfo like
    def test_download_file(self):
        from FileGrabber.info import File
        url = r'https://media2.giphy.com/media/Lo3ye2DFiXN9C/giphy.gif'
        fi = File(url, None)
        # 1 when invalid file
        try:
            filegrabber.download_file(None)
            self.assertTrue(False)
        except AttributeError:
            self.assertTrue(True)

        # 2 check result
        dl_rslt = filegrabber.download_file(fi)
        self.assertEqual(fi.PATH, dl_rslt[0])

if __name__ == '__main__':
    unittest.main()
