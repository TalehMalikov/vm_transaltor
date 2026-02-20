class Parser:
    def __init__(self, filename):
        """
        Initializes the Parser object by reading the VM file and storing the commands.
        
        Parameters:
            filename: str - The path to the VM file to be parsed.
            
        Returns:
            None, but initializes self.commands and self.current for parsing.
        """
        self.commands = []
        self.current = -1
        
        with open(filename, 'r') as f:
            for line in f.readlines():
                # remove comments and whitespace
                line = line.split('//')[0].strip()
                # skip empty lines
                if line:
                    self.commands.append(line)
    
    def has_more_lines(self):
        """
        Function that checks if there are more lines to process in the VM file.

        Parameters:
            None, works based on self.current and self.commands
            
        Returns:
            bool - True if there are more lines to process, False otherwise.
        """       
        return self.current < len(self.commands) - 1
    
    def advance(self):
        """
        Function that advances to the next line in the VM file.

        Parameters:
            None, works based on self.current
            
        Returns:
            str - The next command in the VM file.
        """       
        self.current += 1
        return self.commands[self.current]
    
    def command_type(self):
        """
        Function that determines the type of the current command in the VM file.

        Parameters:
            None, works based on self.current
            
        Returns:
            str - The type of the current command in the VM file.
        """          
        cmd = self.commands[self.current].split()[0]
        if cmd == 'push':
            return 'C_PUSH'
        elif cmd == 'pop':
            return 'C_POP'
        elif cmd in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return 'C_ARITHMETIC'
        
        elif cmd == 'label':
            return 'C_LABEL'
        elif cmd == 'goto':
            return 'C_GOTO'
        elif cmd == 'if-goto':
            return 'C_IF'
        
        elif cmd == 'function':
            return 'C_FUNCTION'
        elif cmd == 'call':
            return 'C_CALL'
        elif cmd == 'return':
            return 'C_RETURN'
    
    def segment(self):
        """
        Function that returns the segment of the current command in the VM file.

        Parameters:
            None, works based on self.current

        Returns:
            str - The segment of the current command in the VM file.
        """
        return self.commands[self.current].split()[1]
    
    def index(self):
        """
        Function that returns the index of the current command in the VM file.

        Parameters:
            None, works based on self.current
        
        Returns:
            str - The index of the current command in the VM file.
        """
        return self.commands[self.current].split()[2]
    
    def command(self):
        """
        Function that returns the current command in the VM file.

        Parameters:
            None, works based on self.current

        Returns:
            str - The current command in the VM file.
        """
        return self.commands[self.current].split()[0]