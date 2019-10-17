import unittest
import re
from FileGrabber.handler import grabbers
from test.ForTest import FileGrabberTestMain


class CasesClien(object):
    NG = 'ng'
    MP4_FILE = 'mp4_file'
    MP4_FILES = 'mp4_files'
    GIF_FILES = 'gif_files'


class GrabbersTest(FileGrabberTestMain):
    def test_getBsobj(self):
        from bs4 import BeautifulSoup
        url = r'https://www.clien.net/service/board/park/13514749'
        result = grabbers.Grabbers.get_bsobj(url)
        # 1 Return should be not none
        self.assertIsNotNone(result)
        # 2 return should be type of bs
        self.assertIsInstance(result, BeautifulSoup)

        # 3 if url is invalid method should throw value error
        url = r'about:blank'
        try:
            grabbers.Grabbers.get_bsobj(url)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)


class ClienTest(FileGrabberTestMain):
    @classmethod
    def setUpClass(cls):
        cls.module = grabbers.Clien()
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


class TheqooTest(FileGrabberTestMain):
    @classmethod
    def setUpClass(cls):
        cls.module = grabbers.Theqoo()
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
                r'https://theqoo.net/1110055038',
                r'https://theqoo.net/1110055038?abcde')
        for url in urls:
            reform = self.module.reformat_url(url)
            result = re.compile('^http(s)?://theqoo\.net/[\d]{8,15}/$').match(reform)
            self.assertIsNotNone(result)
        # NG
        url = r'https://theqoo.net/index.php'
        try:
            self.module.reformat_url(url)
        except ValueError:
            pass

    def test_convert_gfycat(self):
        cases = ({'asis': r'https://gfycat.com/WelldocumentedBlackandwhiteGartersnake',
                  'tobe': r'https://thumbs.gfycat.com/WelldocumentedBlackandwhiteGartersnake-size_restricted.gif'},
                 {'asis': r'https://giant.gfycat.com/PinkTightCrustacean.webm',
                  'tobe': r'https://thumbs.gfycat.com/PinkTightCrustacean-size_restricted.gif'})
        for case in cases:
            result = grabbers.Theqoo.convert_gfycat(case['asis'])
            self.assertEqual(case['tobe'], result)


class CasesInstagram(object):
    NG = 'ng'
    A_PHOTO = 'a_photo'
    PHOTOS = 'photos'
    VIDEO = 'video'
    MIXED = 'mixed'


# Todo : way of bs_obj's refreshment.
class InstagramTest(FileGrabberTestMain):
    @classmethod
    def setUpClass(cls):
        cls.module = grabbers.Instagram()
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
                cls.url_list_json[case] = cls.module.reformat_url(url)
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
            reform = self.module.reformat_url(url)
            result = re.compile(pattern).match(reform)
            self.assertIsNotNone(result)
        # NG
        url = r'https://www.instagram.com/kyokofukada_official/'
        try:
            grabbers.Instagram.reformat_url(url)
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
