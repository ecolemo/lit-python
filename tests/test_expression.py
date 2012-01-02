import unittest
from template import Template

class TestExpression(unittest.TestCase):
    
    def test_plaintext(self):
        text = u'''

abc
   def

qwer
  
x
'''
        self.assertEqual(text, Template(text=text).render())
        
    def test_expression(self):
        text = u'''
lit is <%= 'language independent template' %>

number: <%= 6 %>

expression: <%= {'a':5}['a']
 + 4 %> == 9
'''
        self.assertEquals(u'''
lit is language independent template

number: 6

expression: 9 == 9
''', Template(text=text).render())
        
    def test_context(self):
        text = u'''show <%= a %> <%= b %>'''
        self.assertEqual('show 5 Hello', Template(text=text).render(a=5, b='Hello'))
        
    def test_scriptlet(self):
        text = u'''
<%
    a = 0
    for i in [1, 2, 3, 4]:
        a = a + i
%>
a = <%= 10 %>
'''
        self.assertEqual(u'\n\na = 10\n', Template(text=text).render())
    
    def test_forloop(self):
        text = u'''
<% for i in [1, 2, 3, 4]: %>
loop <%= i %>
<% end %>'''
        
        self.assertEqual(u'''

loop 1
loop 2
loop 3
loop 4        
''', Template(text=text).render())