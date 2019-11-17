import unittest
import os
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup


class FileGrabberTestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @staticmethod
    def print_caller(self):
        print('Test : ' + sys._getframe(1).f_code.co_name, end='')

    @staticmethod
    # Todo: change method name to prepare_bsobjects
    def prepare_testenv(url_list, testenv_dir=None):
        if testenv_dir is None:
            testenv_dir = r'.test/testenv/'
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