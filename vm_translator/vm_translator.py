import os

from vm_translator.code_writer import CodeWriter
from vm_translator.parser import Parser

class VMTranslator:
    def __init__(self):
        """
        Initializes the VMTranslator object with attributes for the parser and code writer.
        
        Parameters:
            None, but sets up self.parser and self.code_writer for use in translation.
        
        Returns:
            None, but initializes self.parser and self.code_writer for the translation process.
        """
        self.parser : Parser
        self.code_writer : CodeWriter
        
    def write_folder(self, foldername):
        """
        Function that handles the translation of all VM files in a given folder.
        
        Parameters:
            foldername: str - The path to the folder containing VM files to be translated.
            
        Returns:
            None, but translates all VM files in the specified folder and writes the output to a single assembly file.
        """
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
        """
        Function that writes the bootstrap code to the output assembly file before translating any VM commands.

        Parameters:
            None, but writes the bootstrap code to the output file to set up the initial state of the VM.
        
        Returns:
            None, but writes the bootstrap code to the output file to initialize the stack pointer and call Sys.init.
        """
        self.code_writer.write_init()

    
    def write_file(self, filename):
        """
        Function that handles the translation of a single VM file.

        Parameters:
            filename: str - The path to the VM file to be translated.

        Returns:
            None, but translates the specified VM file and writes the output to a corresponding assembly file.
        """
        self.parser = Parser(filename)
        self.code_writer = CodeWriter(filename.replace('.vm', '.asm'))
        
        self._translate()
        self.code_writer.close()


    def _translate(self):
        """
        Private function that performs the actual translation of VM commands to assembly code by iterating through the commands in the parser and writing the corresponding assembly code using the code writer.
        
        Parameters:
            None, but works based on the current state of self.parser and self.code_writer to translate VM commands to assembly code.
        
        Returns:
            None, but translates the VM commands from the parser and writes the corresponding assembly code to the output file using the code writer.
        """
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