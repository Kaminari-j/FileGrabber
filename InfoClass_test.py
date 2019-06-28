import unittest
import InfoClass


class TestWebSites(unittest.TestCase):
    def test_get_websites_dict(self):
        exp = set()
        exp.add(InfoClass.Websites.THEQOO)
        exp.add(InfoClass.Websites.CLIEN)
        result = InfoClass.Websites.get_websites_dict()
        self.assertEqual(exp, set(result.values()))

