import os

from vm_translator.code_writer import CodeWriter
from vm_translator.parser import Parser

class VMTranslator:
    def __init__(self):
        self.parser : Parser
        self.code_writer : CodeWriter
        
    def write_folder(self, foldername):
        output = os.path.join(foldername, os.path.basename(foldername.rstrip('/')) + '.asm')
        self.code_writer = CodeWriter(output)  # one shared output file
        self.write_bootstrap()

        for f in os.listdir(foldername):
            if f.endswith('.vm'):
                self.parser = Parser(os.path.join(foldername, f))
                self.code_writer.set_filename(f.replace('.vm', ''))  # add this!
                self._translate()
                
        self.code_writer.close()


    def write_bootstrap(self):
        self.code_writer.write_init()

    
    def write_file(self, filename):
        self.parser = Parser(filename)
        self.code_writer = CodeWriter(filename.replace('.vm', '.asm'))
        
        self._translate()
        self.code_writer.close()


    def _translate(self):
        while self.parser.has_more_lines():
            self.parser.advance()
            
            if self.parser.command_type() == 'C_PUSH':
                self.code_writer.write_push(self.parser.segment(), self.parser.index())
            elif self.parser.command_type() == 'C_POP': 
                self.code_writer.write_pop(self.parser.segment(), self.parser.index())
            elif self.parser.command_type() == 'C_ARITHMETIC':
                self.code_writer.write_arithmetic(self.parser.command())

            elif self.parser.command_type() == 'C_LABEL':
                self.code_writer.write_label(self.parser.segment())
            elif self.parser.command_type() == 'C_GOTO':
                self.code_writer.write_goto(self.parser.segment())
            elif self.parser.command_type() == 'C_IF':

                self.code_writer.write_if(self.parser.segment())
            elif self.parser.command_type() == 'C_FUNCTION':
                self.code_writer.write_function(self.parser.segment(), self.parser.index())
            elif self.parser.command_type() == 'C_CALL':
                self.code_writer.write_call(self.parser.segment(), self.parser.index())
            elif self.parser.command_type() == 'C_RETURN':
                self.code_writer.write_return()