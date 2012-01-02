from pyparsing import Literal, SkipTo, Word, OneOrMore, Regex, alphanums, \
    QuotedString, White
from types import ModuleType
import re

class Template(object):
    
    def __init__(self, text='', filename='', lookup=None):
        self.module_id = "memory:" + hex(id(self))
        self.source = text
        self.declarations = []
        self.class_definition = ''
        self.source_lines = '''
def render_body(out):
'''.splitlines()
        self.indent = 1
        
        template_close = Literal('%>')
        
        white = OneOrMore(White())
        
        properties = Word(alphanums + '_') + Word(alphanums + '_') + Literal('=') + QuotedString('"')
        directive = "<%@" + white + properties + white + template_close
        declaration = "<%!" + SkipTo(template_close) + template_close
        expression = "<%=" + SkipTo(template_close) + template_close
        scriptlet = '<%' + SkipTo(template_close) + template_close
        
        template_text = directive | declaration | expression |  scriptlet
        plain_text = Regex(r'((?!<%).|\s)+', re.MULTILINE)
        
        body = template_text | plain_text
        lit = OneOrMore(body)
        
        directive.setParseAction(self.compile_directive)
        declaration.setParseAction(self.compile_declaration)
        expression.setParseAction(self.compile_expression)
        scriptlet.setParseAction(self.compile_scriptlet)
        plain_text.setParseAction(self.compile_plain_text)
        lit.setParseAction(self.compile_all)
        lit.leaveWhitespace()

        lit.parseString(self.source)
        self.out = TemplateOutput()
        
    def compile_all(self, s, loc, token):
        print loc, token
        
    def compile_directive(self, s, loc, tokens):
        print 'directive'
        self.source_lines.insert(0, '@@@@@' + tokens[1])
    
    def compile_declaration(self, s, loc, tokens):
        print 'declaration'
        self.source_lines.insert(0, '!!!!!' + tokens[1])
    
    def compile_scriptlet(self, s, loc, tokens):
        lines = tokens[1].splitlines()
        indent_set = False
        firstline_indent = 0
        for line in lines:
            if not indent_set:
                m = re.search(r'\S', line)
                if m: 
                    firstline_indent = m.start()
                    indent_set = True
                
                    
            self.source_lines.append(' ' * self.indent * 4 + line[firstline_indent:])
    
    def compile_expression(self, s, loc, tokens):
        self.source_lines.append(' ' * self.indent * 4 + "out.write(" + tokens[1] + ")")
        
    def compile_plain_text(self, s, loc, tokens):
        self.source_lines.append(' ' * self.indent * 4 + "out.write('''" + tokens[0] + "''')") 
        
    def render(self, **kwargs):
        self.module_source = '\n'.join(self.source_lines)
        print self.module_source
        self.code = compile(self.module_source, self.module_id, 'exec')
        self.module = ModuleType(self.module_id)
        self.module.__dict__.update(kwargs)
        
        exec self.code in self.module.__dict__, self.module.__dict__
        self.module.render_body(self.out)
        return self.out.output

class TemplateOutput(object):
    def __init__(self):
        self.output = u''
    def write(self, text):
        self.output += unicode(text)

#print '\n'.join(Template('test.lit').source_lines)

