import unittest
import re
import sys
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
from FileGrabber import FileGrabber
import FileGrabberModule
from InfoClass import FileInfo, Websites


class FileGrabberTestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raise NotImplementedError

    @staticmethod
    def print_caller(self):
        print('Test : ' + sys._getframe(1).f_code.co_name, end='')

    @staticmethod
    # Todo: change method name to prepare_bsobjects
    def prepare_testenv(url_list, testenv_dir=None):
        if testenv_dir is None:
            testenv_dir = r'./testenv/'
        if not os.path.exists(testenv_dir):
            os.makedirs(testenv_dir)

        bs_list = dict()
        for key, value in url_list.items():
            path = testenv_dir + key

            if not os.path.exists(path):
                html = urlopen(value)
                # Save HTML to a file
                with open(path, "wb") as f:
                    while True:
                        chunk = html.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)

            # Read HTML from a file
            with open(path, "rb") as f:
                bs_list[key] = BeautifulSoup(f.read(), features="html.parser")

        return bs_list

    @classmethod
    def tearDownClass(cls):
        if sys.flags.debug: print('> tearDownClass method is called.')
        # setUpClassで準備したオブジェクトを解放する
        cls.CLS_VAL = '> tearDownClass : released!'
        if sys.flags.debug: print(cls.CLS_VAL)


class test_Common(FileGrabberTestMain):
    @classmethod
    def setUpClass(cls):
        pass

    # @unittest.skip("bs obj取得に時間がかかるため、普段はスキップする")
    def test_getBsobj(self):
        url = r'https://www.clien.net/service/board/park/13514749'
        result = FileGrabberModule.Common.getBsobj(url)
        # 1 Return should be not none
        self.assertIsNotNone(result)
        # 2 return should be type of bs
        self.assertIsInstance(result, BeautifulSoup)

        # 3 if url is invalid method should throw value error
        url = r'about:blank'
        try:
            FileGrabberModule.Common.getBsobj(url)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    # Todl: change method name to file_download_with_FileInfo like
    def test_file_download(self):
        url = r'https://media2.giphy.com/media/Lo3ye2DFiXN9C/giphy.gif'
        fi = FileInfo(url, None)
        # 1 when invalid file
        try:
            FileGrabberModule.Common.download(None)
            self.assertTrue(False)
        except AttributeError:
            self.assertTrue(True)

        # 2 check result
        dl_rslt = FileGrabberModule.Common.download(fi)
        self.assertEqual(fi.PATH, dl_rslt[0])

    def test_verify_website(self):
        with self.assertRaises(ValueError):
            FileGrabberModule.Common.verify_website('https://www.naver.com')

        urls = {'clien': r'https://www.clien.net/service/board/park',
                'theqoo': r'https://theqoo.net/index.php?mid=square&filter_mode=normal&page=2&document_srl=1110055038'}
        for site, url in urls.items():
            result = FileGrabberModule.Common.verify_website(url)
            self.assertIsNotNone(result)
            if site == Websites.CLIEN:
                self.assertEqual(result, Websites.CLIEN)
            elif site == Websites.THEQOO:
                self.assertEqual(result, Websites.THEQOO)


class CasesClien(object):
    NG = 'ng'
    MP4_FILE = 'mp4_file'
    MP4_FILES = 'mp4_files'
    GIF_FILES = 'gif_files'


class test_Clien(FileGrabberTestMain):
    @classmethod
    def setUpClass(cls):
        cls.filegrabber = FileGrabber()
        cls.module = FileGrabberModule.Clien()
        cls.url_list = {
            CasesClien.NG: 'https://www.clien.net/service/board/park/13511316',
            CasesClien.MP4_FILE: 'https://www.clien.net/service/board/park/13514749',
            CasesClien.MP4_FILES: 'https://www.clien.net/service/board/park/13516328',
            CasesClien.GIF_FILES: 'https://www.clien.net/service/board/park/13519036'
        }
        cls.bs_list = cls.prepare_testenv(cls.url_list, r'./testenv/clien/')
        # create articles
        cls.articles = dict()
        try:
            for case, bsobj in cls.bs_list.items():
                cls.articles[case] = cls.module.get_article(bsobj)
        except:
            import traceback
            traceback.print_exc()
            cls.articles = None

    def test_get_article(self):
        self.assertIsNone(self.module.get_article(None))
        self.assertIsNone(self.module.get_article('test'))
        self.assertIsNotNone(self.module.get_article(self.bs_list[CasesClien.MP4_FILE]))

    def test_collect_files_from_article(self):
        for case, article in self.articles.items():
            result = self.module.collect_files_from_article(article)
            # Case: NG
            if case == CasesClien.NG:
                self.assertIsNone(result)
            # Case: OK
            else:
                self.assertIsNotNone(result)
                self.assertIsInstance(result, list)
                self.assertIsInstance(result[0], str)

                pattern = 'http(s)?://.*\.(gif|mp4)'
                for file in result:
                    self.assertIsNotNone(re.compile(pattern).match(file))


class CasesTheqoo(object):
    NG = 'ng'
    GFY_FILE = 'gfy_file'
    GFY_FILES = 'gfy_files'
    GIF_FILES = 'gif_files'


class test_Theqoo(FileGrabberTestMain):
    @classmethod
    def setUpClass(cls):
        cls.filegrabber = FileGrabber()
        cls.module = FileGrabberModule.Theqoo()
        cls.url_list = {
            'ng': 'https://theqoo.net/1111082289',
            'gfy_file': 'https://theqoo.net/1111082407',
            'gfy_files': 'https://theqoo.net/1110148231',
        }
        cls.bs_list = cls.prepare_testenv(cls.url_list, r'./testenv/theqoo/')
        # create articles
        cls.articles = dict()
        try:
            for case, bsobj in cls.bs_list.items():
                cls.articles[case] = cls.module.get_article(bsobj)
        except:
            import traceback
            traceback.print_exc()
            cls.articles = None

    def test_get_article(self):
        self.assertIsNone(self.module.get_article(None))
        self.assertIsNone(self.module.get_article('test'))
        self.assertIsNotNone(self.module.get_article(self.bs_list[CasesTheqoo.GFY_FILE]))

    def test_collect_files_from_article(self):
        for case, article in self.articles.items():
            result = self.module.collect_files_from_article(article)
            # Case: NG
            if case == CasesTheqoo.NG:
                self.assertIsNone(result)
            # Case: OK
            else:
                self.assertIsNotNone(result)
                self.assertIsInstance(result, list)
                self.assertIsInstance(result[0], str)

                '''
                http(s)?://gfycat\.com/\D+
                pattern = 'http(s)?://.*\.(gif|mp4)'
                for file in result:
                    self.assertIsNotNone(re.compile(pattern).match(file))
                '''

    def test_reformat_url(self):
        # OK
        urls = (r'https://theqoo.net/index.php?mid=square&filter_mode=normal&page=2&document_srl=1110055038',
                r'https://theqoo.net/index.php?mid=square&filter_mode=normal&page=2&document_srl=1110055039',
                r'https://theqoo.net/1110055038')
        pattern = '^http(s)?://theqoo\.net/[0-9]+$'
        for url in urls:
            reform = FileGrabberModule.Theqoo.reformat_url(url)
            result = re.compile(pattern).match(reform)
            self.assertIsNotNone(result)
        # NG
        url = r'https://theqoo.net/index.php'
        try:
            FileGrabberModule.Theqoo.reformat_url(url)
        except ValueError:
            pass

    def test_convert_gfycat(self):
        cases = ({'asis': r'https://gfycat.com/WelldocumentedBlackandwhiteGartersnake',
                  'tobe': r'https://thumbs.gfycat.com/WelldocumentedBlackandwhiteGartersnake-size_restricted.gif'},
                 {'asis': r'https://giant.gfycat.com/PinkTightCrustacean.webm',
                  'tobe': r'https://thumbs.gfycat.com/PinkTightCrustacean-size_restricted.gif'})
        for case in cases:
            result = FileGrabberModule.Theqoo.convert_gfycat(case['asis'])
            self.assertEqual(case['tobe'], result)


class CasesInstagram(object):
    NG = 'ng'
    A_PHOTO = 'a_photo'
    PHOTOS = 'photos'
    VIDEO = 'video'
    MIXED = 'mixed'


# Todo : way of bs_obj's refreshment.
class test_Instagram(FileGrabberTestMain):
    @classmethod
    def setUpClass(cls):
        cls.filegrabber = FileGrabber()
        cls.module = FileGrabberModule.Instagram()
        cls.url_list = {
            'ng': 'https://www.instagram.com/kyokofukada_official/',
            'a_photo': 'https://www.instagram.com/p/BWJUqO6jXpy/?utm_source=ig_web_button_share_sheet',
            'photos': 'https://www.instagram.com/p/Br84A_jFDVC/',
            'video': 'https://www.instagram.com/p/BWREXKfj-35/',
            'mixed': 'https://www.instagram.com/p/BvieWn7lLKR/'
        }
        cls.url_list_json = dict()
        for case, url in cls.url_list.items():
            if case != 'ng':
                cls.url_list_json[case] = FileGrabberModule.Instagram.reformat_url(url)
        cls.bs_list = cls.prepare_testenv(cls.url_list_json, r'./testenv/instagram/')
        # create articles
        cls.articles = dict()
        try:
            for case, bsobj in cls.bs_list.items():
                cls.articles[case] = cls.module.get_article(bsobj)
        except:
            import traceback
            traceback.print_exc()
            cls.articles = None

    def test_reformat_url(self):
        # OK
        urls = (r'https://www.instagram.com/p/BWJUqO6jXpy/?utm_source=ig_web_button_share_sheet',
                r'https://www.instagram.com/p/Br84A_jFDVC/',
                r'https://www.instagram.com/p/BvieWn7lLKR',
                r'https://www.instagram.com/p/BvieWn7lLKR//',
                r'https://www.instagram.com/p/BWREXKfj-35/',
                r'https://www.instagram.com/p/BWREXKfj-35')
        pattern = '^http(s)?://www\.instagram\.com/p/[\w|-]+/\?__a=1$'
        for url in urls:
            reform = FileGrabberModule.Instagram.reformat_url(url)
            result = re.compile(pattern).match(reform)
            self.assertIsNotNone(result)
        # NG
        url = r'https://www.instagram.com/kyokofukada_official/'
        try:
            FileGrabberModule.Instagram.reformat_url(url)
        except TypeError:
            pass

    def test_get_article(self):
        self.assertIsNone(self.module.get_article(None))
        self.assertIsNone(self.module.get_article('test'))
        self.assertIsNotNone(self.module.get_article(self.bs_list[CasesInstagram.A_PHOTO]))

    def test_collect_files_from_article(self):
        for case, article in self.articles.items():
            result = self.module.collect_files_from_article(article)
            # Case: NG
            if case == CasesInstagram.NG:
                self.assertIsNone(result)
            # Case: OK
            else:
                self.assertIsNotNone(result)
                self.assertIsInstance(result, list)
                self.assertIsInstance(result[0], str)


if __name__ == '__main__':
    unittest.main()
