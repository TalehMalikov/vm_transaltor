from vm_translator.code_writer import CodeWriter
from vm_translator.parser import Parser

class VMTranslator:
    def __init__(self, input_file):
        self.parser = Parser(input_file)
        self.code_writer = CodeWriter(input_file.replace('.vm', '.asm'))
    
    def translate(self):
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

        self.code_writer.close()