from pyparsing import Literal, OneOrMore, White, Word, alphanums, QuotedString, \
    SkipTo, Regex, ZeroOrMore, Optional
import re

class TemplateParser(object):
    def translate(self, text, filename):
        self.source = text
        self.declaration = '''
'''
        self.block_lines = []
        self.source_lines = '''
def render_body():
'''.splitlines()

        self.target_lines = self.source_lines
        self.indent = 1
        
        template_close = Literal('%>')
        white = White()
        
        attribute = Word(alphanums + '_') + Literal('=') + QuotedString('"') + Optional(white)
        
        directive = "<%@" +  Optional(white) + Word(alphanums + '_') + white + ZeroOrMore(attribute) + template_close
        declaration = "<%!" + SkipTo(template_close) + template_close
        expression = "<%=" + SkipTo(template_close) + template_close
        scriptlet = '<%' + SkipTo(template_close) + template_close
        
        template_text = directive | declaration | expression | scriptlet
        plain_text = Regex(r'((?!<%).|\s)+', re.MULTILINE)
        
        body = template_text | plain_text
        lit = OneOrMore(body)
        
        directive.setParseAction(self.compile_directive)
        declaration.setParseAction(self.compile_declaration)
        expression.setParseAction(self.compile_expression)
        scriptlet.setParseAction(self.compile_scriptlet)
        plain_text.setParseAction(self.compile_plain_text)
        
        lit.leaveWhitespace()
        lit.parseString(self.source)
        
        translated = self.declaration + '\n'.join(self.block_lines + ['\n'] + self.source_lines)
        print translated
        return translated
        
    def compile_directive(self, s, loc, tokens):
        tokens = filter(lambda token:not re.match(r'\s|=', token), tokens[1:-1])
        # TODO attributes to dict
        getattr(self, 'process_' + tokens[0])(tokens[1:])
    
    def process_block(self, tokens):
        if tokens[0] == 'name':
            name = tokens[1]

        self.printline('render_%s()' % name)

        self.target_lines = self.block_lines        
        self.indent = 0
        self.printline('def render_%s():' % name)
        self.indent += 1
    
    def process_endblock(self, tokens):
        self.target_lines = self.source_lines
        self.indent = 1
    
    def process_include(self, tokens):
        pass
    
    def compile_declaration(self, s, loc, tokens):
        print 'declaration'
        self.source_lines.insert(0, '!!!!!' + tokens[1])
    
    def compile_scriptlet(self, s, loc, tokens):
        lines = tokens[1].splitlines()
        indent_set = False
        indent_next = 0
        firstline_indent = 0
        for line in lines:
            m = re.search(r'\S', line)
            if not indent_set and m: 
                firstline_indent = m.start()
                indent_set = True
                    
            if m and line.rstrip().endswith(':'):
                indent_next = 1
            else:
                indent_next = 0
            
            if line.strip() == '# end':
                indent_next = -1

            self.printline(line[firstline_indent:])
        
        self.indent += indent_next
    
    def compile_expression(self, s, loc, tokens):
        self.printline("out.write(" + tokens[1] + ")")
        
    def compile_plain_text(self, s, loc, tokens):
        self.printline("out.write('''" + tokens[0] + "''')") 

    def printline(self, line):
        self.target_lines.append(' ' * self.indent * 4 + line)