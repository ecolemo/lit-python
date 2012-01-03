import unittest
from lit.template import Template

class TestScriptlet(unittest.TestCase):
    def test_scriptlet(self):
        text = u'''
<%
    a = 0
    for i in [1, 2, 3, 4]:
        a = a + i
%>
a = <%= 10 %>
'''
        template = Template(text=text)
        self.assertEqual(u'\n\na = 10\n', template.render())
    
    def test_forloop(self):
        text = u'''
<%
s = 0
for i in [1, 2, 3, 4]: %>
loop <%= i %><% s = s + i %>
<%# end %>
sum = <%= s %>'''
        
        self.assertEqual(u'''

loop 1

loop 2

loop 3

loop 4

sum = 10''', Template(text=text).render())
        
    def test_if(self):
        text = u'''<% if True: %><%= 1 %><%# end%><% else: %><%= 0 %><% end %>'''
        self.assertEqual(u'''1''', Template(text=text).render())
        
    def test_function(self):
        text = u'''
<% def embed(): %>
hello
<%# end %>

<% embed() %>'''
        print Template(text=text).module_source
        self.assertEqual(u'''hello''', Template(text=text).render().strip())
        