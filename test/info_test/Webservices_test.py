import unittest
from FileGrabber.info import Webservices


class Test(unittest.TestCase):
    def test_get_webservices_dict(self):
        exp = set()
        exp.add(Webservices.THEQOO)
        exp.add(Webservices.CLIEN)
        exp.add(Webservices.INSTAGRAM)
        result = Webservices.get_webservices_dict()
        self.assertEqual(exp, set(result.values()))

