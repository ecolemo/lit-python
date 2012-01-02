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
