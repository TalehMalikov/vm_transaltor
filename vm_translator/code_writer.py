from vm_translator.translations import Translations

class CodeWriter:
    def __init__(self, filename):
        """
        Initializes the CodeWriter object by opening the output file and setting up necessary attributes.
        
        Parameters:
            filename: str - The path to the output assembly file to be written.
        
        Returns:
            None, but initializes self.file, self.label_counter, self.translations, and self.filename for code writing.
        """
        self.file = open(filename, 'w')
        self.label_counter = 0  # for unique labels in eq, gt, lt
        self.translations = Translations()
        self.filename = 'Static'

    def set_filename(self, filename):
        """
        Sets the current filename for static variable handling in the CodeWriter.

        Parameters:
            filename: str - The name of the current VM file being translated.

        Returns:
            None, but updates self.filename for static variable handling.
        """
        self.filename = filename

    def write_init(self):
        """
        Function that writes the bootstrap code to the output assembly file.
        
        Parameters:
            None
        
        Returns:
            None, but writes the bootstrap code to the output file.
        """
        asm = '@256\nD=A\n@SP\nM=D\n'
        asm += self.translations.WriteCall('Sys.init', 0, label_counter=self.label_counter)
        self.label_counter += 1
        self.file.write(asm + '\n')

    def write_push(self, segment, index):
        """
        Function that writes the assembly code for a push command to the output file.

        Parameters:
            segment: str - The segment to push from.
            index: int - The index within the segment.

        Returns:
            None, but writes the assembly code for the push command to the output file.
        """
        asm = self.translations.Push(segment, index, self.filename)
        self.file.write(asm + '\n')

    def write_pop(self, segment, index):
        """
        Function that writes the assembly code for a pop command to the output file.

        Parameters:
            segment: str - The segment to pop to.
            index: int - The index within the segment.
        
        Returns:
            None, but writes the assembly code for the pop command to the output file.
        """
        asm = self.translations.Pop(segment, index, self.filename)
        self.file.write(asm + '\n')

    def write_arithmetic(self, cmd):
        """
        Function that writes the assembly code for an arithmetic command to the output file.

        Parameters:
            cmd: str - The arithmetic command (e.g., 'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not').
        
        Returns:
            None, but writes the assembly code for the arithmetic command to the output file.
        """
        asm = ''
        if cmd == 'add':
            asm = self.translations.Add()
        elif cmd == 'sub':
            asm = self.translations.Sub()
        elif cmd == 'neg':
            asm = self.translations.Neg()
        elif cmd == 'eq':
            asm = self.translations.Compare('JEQ', self.label_counter)
            self.label_counter += 1
        elif cmd == 'gt':
            asm = self.translations.Compare('JGT', self.label_counter)
            self.label_counter += 1
        elif cmd == 'lt':
            asm = self.translations.Compare('JLT', self.label_counter)
            self.label_counter += 1
        elif cmd == 'and':
            asm = self.translations.And()
        elif cmd == 'or':
            asm = self.translations.Or()
        elif cmd == 'not':
            asm = self.translations.Not()
        self.file.write(asm + '\n')

    def write_label(self, label):
        """
        Function that writes the assembly code for a label command to the output file.
        
        Parameters:
            label: str - The label name to be defined in the assembly code.
        
        Returns:
            None, but writes the assembly code for the label command to the output file.
        """
        asm = self.translations.Label(label)
        self.file.write(asm + '\n')
    
    def write_goto(self, label):
        """
        Function that writes the assembly code for a goto command to the output file.
        
        Parameters:
            label: str - The label name to jump to in the assembly code.
        
        Returns:
            None, but writes the assembly code for the goto command to the output file.
        """
        asm = self.translations.Goto(label)
        self.file.write(asm + '\n')
    
    def write_if(self, label):
        """
        Function that writes the assembly code for an if-goto command to the output file.

        Parameters:
            label: str - The label name to conditionally jump to in the assembly code.
        
        Returns:
            None, but writes the assembly code for the if-goto command to the output file.
        """
        asm = self.translations.IfGoto(label)
        self.file.write(asm + '\n')

    def write_function(self, function_name, num_locals):
        """
        Function that writes the assembly code for a function declaration command to the output file.

        Parameters:
            function_name: str - The name of the function being declared.
            num_locals: int - The number of local variables for the function.

        Returns:
            None, but writes the assembly code for the function declaration command to the output file.
        """
        asm = self.translations.WriteFunction(function_name, num_locals)
        self.file.write(asm + '\n')
    
    def write_call(self, function_name, num_args):
        """
        Function that writes the assembly code for a function call command to the output file.

        Parameters:
            function_name: str - The name of the function being called.
            num_args: int - The number of arguments being passed to the function.
        
        Returns:
            None, but writes the assembly code for the function call command to the output file.
        """
        asm = self.translations.WriteCall(function_name, num_args, label_counter=self.label_counter)
        self.label_counter += 1
        self.file.write(asm + '\n')

    def write_return(self):
        """
        Function that writes the assembly code for a return command to the output file.

        Parameters:
            None
        
        Returns:
            None, but writes the assembly code for the return command to the output file.
        """
        asm = self.translations.WriteReturn()
        self.file.write(asm + '\n')

    def close(self):
        """
        Function that writes the end of the assembly code and closes the output file.
        
        Parameters:
            None
        
        Returns:
            None, but writes the end of the assembly code and closes the output file.
        """
        self.file.write('(END)\n@END\n0;JMP\n')
        self.file.close()