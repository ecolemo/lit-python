from lit.template import Template, TemplateLookup
import unittest
import os

class TestInheritance(unittest.TestCase):
    def test_block(self):
        text = '''
<%@ block name="header" %>
header
<%@ endblock %>

body
'''
        self.assertEquals('\n\nheader\n\n\nbody\n', Template(text).render())
        
    def atest_include(self):
        lookup = TemplateLookup()
        text = '''
<p>
<%@ include name="hello.html" %>
</p>'''
        self.assertEquals('''
<p>
Hello
</p>''', Template(text, lookup=lookup).render())