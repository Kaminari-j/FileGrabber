import unittest
from FileGrabber.modules import InfoClass


class TestWebSites(unittest.TestCase):
    def test_get_websites_dict(self):
        exp = set()
        exp.add(InfoClass.Websites.THEQOO)
        exp.add(InfoClass.Websites.CLIEN)
        exp.add(InfoClass.Websites.INSTAGRAM)
        result = InfoClass.Websites.get_websites_dict()
        self.assertEqual(exp, set(result.values()))
