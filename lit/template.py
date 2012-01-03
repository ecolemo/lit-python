from lit.parser import TemplateParser
from types import ModuleType
import os

class Template(object):
    
    def __init__(self, text='', filename='', lookup=None):
        if filename: text = open(filename, 'r').read()
        self.source = text
        self.module_source = TemplateParser().translate(text, filename)
        self.module_id = "memory:" + hex(id(self))
        self.code = compile(self.module_source, self.module_id, 'exec')
        self.module = ModuleType(self.module_id)
        
    def render(self, **kwargs):        
        self.module.__dict__.update(kwargs)
        
        exec self.code in self.module.__dict__, self.module.__dict__

        self.module.out = TemplateOutput()
        self.module.render_body()
        return self.module.out.output

class TemplateOutput(object):
    def __init__(self):
        self.output = u''
    def write(self, text):
        self.output += unicode(text)

class TemplateLookup(object):
    
    def __init__(self, directories=[]):
        self.directories = directories
        self.cache = {}

    def __getitem__(self, key):
        if key in self.cache: return self.cache[key]
        
        for directory in self.directories:
            path = directory + os.sep + key
            if os.access(path, os.R_OK): return Template(filename=path, lookup=self)
        raise KeyError(key)
            
    
    def __contains__(self, key):
        if key in self.cache: return True

        for directory in self.directories:
            path = directory + os.sep + key
            if os.access(path, os.R_OK): return True
        return False
    
    def __setitem__(self, key, value):
        self.cache[key] = value

