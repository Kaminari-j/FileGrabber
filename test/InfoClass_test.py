import unittest
from FileGrabber import InfoClass


class TestWebservices(unittest.TestCase):
    def test_get_webservices_dict(self):
        exp = set()
        exp.add(InfoClass.Webservices.THEQOO)
        exp.add(InfoClass.Webservices.CLIEN)
        exp.add(InfoClass.Webservices.INSTAGRAM)
        result = InfoClass.Webservices.get_webservices_dict()
        self.assertEqual(exp, set(result.values()))

