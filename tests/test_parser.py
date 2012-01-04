from lit.parser import list_to_dict
import unittest

class TestParser(unittest.TestCase):
    def test_parse_attribute(self):
        tokens = ['name', 'aaa', 'cache', 'true']
        self.assertEquals({'name': 'aaa', 'cache':'true'}, list_to_dict(tokens))
        