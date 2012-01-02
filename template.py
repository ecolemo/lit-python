from parser import TemplateParser
from types import ModuleType

class Template(object):
    
    def __init__(self, text='', filename='', lookup=None):
        self.module_source = TemplateParser().translate(text, filename)
        print self.module_source

        self.module_id = "memory:" + hex(id(self))
        self.code = compile(self.module_source, self.module_id, 'exec')
        self.module = ModuleType(self.module_id)
        
    def render(self, **kwargs):        
        self.module.__dict__.update(kwargs)
        
        exec self.code in self.module.__dict__, self.module.__dict__

        self.out = TemplateOutput()
        self.module.render_body(self.out)
        return self.out.output

class TemplateOutput(object):
    def __init__(self):
        self.output = u''
    def write(self, text):
        self.output += unicode(text)

#print '\n'.join(Template('test.lit').source_lines)

