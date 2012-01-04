from lit.template import Template, TemplateLookup
import unittest

class TestInheritance(unittest.TestCase):
    def test_block(self):
        text = '''
<%@ block name="header" %>
header
<%@ endblock %>

body
'''
        self.assertEquals('\n\nheader\n\n\nbody\n', Template(text).render())
        
    def test_include(self):
        lookup = TemplateLookup()
        lookup['hello.html'] = Template('Hello', lookup=lookup)
        text = '''
<p>
<%@ include name="hello.html" %>
</p>'''
        self.assertEquals('''
<p>
Hello
</p>''', Template(text, lookup=lookup).render())
        
    
    def test_extends(self):
        lookup = TemplateLookup()
        lookup['layout.html'] = Template('''
<%@ block name="header" %>
<h1>Hello</h1>
<%@ endblock %>

<p><%@ body %></p>
''', lookup=lookup)
        text = '''<%@ extends name="layout.html" %>World'''
        self.assertEquals('''

<h1>Hello</h1>


<p>World</p>
''', Template(text, lookup=lookup).render())
        
    def test_extends_depth(self):
        lookup = TemplateLookup()
        lookup['layout.html'] = Template('''
<%@ block name="header" %>
<h1>Hello</h1>
<%@ endblock %>

<p><%@ body %>!!</p>
''', lookup=lookup)

        lookup['override.html'] = Template('''
<%@ extends name="layout.html" %>
<%@ block name="header" %>
<h1>Hi!!</h1>
<%@ endblock %>

<%@ body %>
''', lookup=lookup)
        
        text = '''<%@ extends name="override.html" %>World'''
        
        self.assertEquals('''

<h1>Hi!!</h1>


<p>World!!</p>
''', Template(text, lookup=lookup).render())
        