import os
import unittest
from test.ForTest import FileGrabberTestMain
from FileGrabber import filegrabber
from FileGrabber.handler import grabbers
from FileGrabber.info import Webservices


# Todo: belows
class Test(FileGrabberTestMain):
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
        # 1 when invalid file
        with self.assertRaises(AttributeError):
            filegrabber.download_file(None)
        # 2 which website blocking urlretreive
        urls = [
            r'https://www.imageupload.net/upload-image/2019/11/17/GIF21.gif',
            r'https://media2.giphy.com/media/Lo3ye2DFiXN9C/giphy.gif'
        ]
        for url in urls:
            fi = File(url, None)
            filegrabber.download_file(fi)
            self.assertTrue(os.path.exists(fi.PATH))

    @unittest.expectedFailure
    def test_do_grab(self):
        # When module occurs exception
        # Todo: get_files, download_file, convertFile method should raise some exception for failing case
        # Todo: and it should have its own testcase
        self.fail()


if __name__ == '__main__':
    unittest.main()
