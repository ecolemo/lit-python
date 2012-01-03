from lit.template import TemplateLookup
import os
import unittest

class TestLookup(unittest.TestCase):
    def test_lookup(self):
        lookup = TemplateLookup(directories=[os.path.dirname(__file__) + os.sep + 'samples'])
        self.assertIn('index.html', lookup)
        self.assertEqual('<html></html>', lookup['index.html'].source)
        
        self.assertNotIn('NonExistingFile', lookup)
        self.assertRaises(KeyError, lookup.__getitem__, 'NonExistingFile')