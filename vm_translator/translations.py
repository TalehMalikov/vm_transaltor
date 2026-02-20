class Translations:
    constants = {
        'push_to_stack': '@SP\nA=M\nM=D\n@SP\nM=M+1',
        'pop_from_stack': '@SP\nAM=M-1\nD=M',
        'seg_ptrs': {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT'
        }
    }

    def __init__(self):
        pass

    def Add(self):
        """
        Function that handles the add operation in the VM.

        Parameters:
            None
            
        Returns:
            str - The assembly code for the add operation.
        """  
        return '@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M'
    
    def Sub(self):
        """
        Function that handles the sub operation in the VM.

        Parameters:
            None
            
        Returns:
            str - The assembly code for the sub operation.
        """  
        return '@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D'
    
    def Neg(self):
        """
        Function that handles the neg operation in the VM.

        Parameters:
            None
            
        Returns:
            str - The assembly code for the neg operation.
        """  
        return '@SP\nA=M-1\nM=-M'
    
    def Compare(self, jump, label_num):
        """
        Function that handles the compare operation in the VM.

        Parameters:
            jump: str - The jump condition (e.g., 'JEQ', 'JGT', 'JLT').
            label_num: int - A unique number to generate labels for the compare operation.
            
        Returns:
            str - The assembly code for the compare operation.
        """          
        return f'@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@TRUE{label_num}\nD;{jump}\n@SP\nA=M-1\nM=0\n@END{label_num}\n0;JMP\n(TRUE{label_num})\n@SP\nA=M-1\nM=-1\n(END{label_num})'
    
    def And(self):
        """
        Function that handles the and operation in the VM.

        Parameters:
            None
            
        Returns:
            str - The assembly code for the and operation.
        """          
        return '@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M'
    
    def Or(self):
        """
        Function that handles the or operation in the VM.

        Parameters:
            None
            
        Returns:
            str - The assembly code for the or operation.
        """          
        return '@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M'
    
    def Not(self):
        """
        Function that handles the not operation in the VM.

        Parameters:
            None

        Returns:
            str - The assembly code for the not operation.
        """           
        return '@SP\nA=M-1\nM=!M'
    
    def Push(self, segment, index, fileName):
        """
        Function that handles the push operation in the VM.

        Parameters:
            segment: str - The segment to push to.
            index: int - The index within the segment.
            fileName: str - The name of the current file (for static variables).
            
        Returns:
            str - The assembly code for the push operation.
        """           
        if segment == 'constant':
            return f'@{index}\nD=A\n{self.constants["push_to_stack"]}'
        elif segment in ['local', 'argument', 'this', 'that']:
            return f'@{index}\nD=A\n@{self.constants["seg_ptrs"][segment]}\nA=M+D\nD=M\n{self.constants["push_to_stack"]}'
        elif segment == 'temp':
            return f'@{index}\nD=A\n@5\nA=A+D\nD=M\n{self.constants["push_to_stack"]}'
        elif segment == 'pointer':
            ptrs = {'0': 'THIS', '1': 'THAT'}
            return f'@{ptrs[index]}\nD=M\n{self.constants["push_to_stack"]}'
        elif segment == 'static':
            return f'@{fileName}.{index}\nD=M\n{self.constants["push_to_stack"]}'
        return '' 
    
    def Pop(self, segment, index, fileName):
        """
        Function that handles the pop operation in the VM.

        Parameters:
            segment: str - The segment to pop from.
            index: int - The index within the segment.
            fileName: str - The name of the current file (for static variables).
            
        Returns:
            str - The assembly code for the pop operation.
        """        
        if segment in ['local', 'argument', 'this', 'that']:
            return f'@{index}\nD=A\n@{self.constants["seg_ptrs"][segment]}\nD=M+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D'
        elif segment == 'temp':
            return f'@{index}\nD=A\n@5\nD=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D'
        elif segment == 'pointer':
            ptrs = {'0': 'THIS', '1': 'THAT'}
            return f'@SP\nAM=M-1\nD=M\n@{ptrs[index]}\nM=D'
        elif segment == 'static':
            return f'@SP\nAM=M-1\nD=M\n@{fileName}.{index}\nM=D'
        return ''  
    
    def Label(self, label):
        """
        Function that handles the declaration of a label in the VM.

        Parameters:
            label: str - The label to declare.
            
        Returns:
            str - The assembly code for the label declaration.
        """        
        return f'({label})'

    def Goto(self, label):
        """
        Function that handles the unconditional goto operation in the VM.

        Parameters:
            label: str - The label to jump to.

        Returns:
            str - The assembly code for the unconditional goto operation.
        """
        return f'@{label}\n0;JMP'
    
    def IfGoto(self, label):
        """
        Function that handles the conditional goto operation in the VM.
    
        Parameters:
            label: str - The label to jump to if the condition is true.
    
        Returns:
            str - The assembly code for the conditional goto operation.
        """
        return f'@SP\nAM=M-1\nD=M\n@{label}\nD;JNE'
    
    def WriteFunction(self, function_name, num_locals):
        """
        Function that handles the declaration of a function in the VM.
    
        Parameters:
            function_name: str - The name of the function.
            num_locals: int - The number of local variables for the function.
    
        Returns:
            str - The assembly code for the function declaration.
        """        
        asm = f'({function_name})\n'
        for i in range(int(num_locals)):
            asm += self.Push('constant', '0','') + '\n'
        return asm
    
    def WriteCall(self, function_name, num_args, label_counter):
        """
        Function that handles the call to a function in the VM.
    
        Parameters:
            function_name: str - The name of the function to call.
            num_args: int - The number of arguments for the function.
            label_counter: int - A counter to generate unique labels.
    
        Returns:
            str - The assembly code for the call operation.
        """
        #push return address
        asm = f'@RETURN_ADDRESS{label_counter}\nD=A\n{self.constants["push_to_stack"]}\n'
        label_counter += 1

        # push LCL, ARG, THIS, THAT
        asm += '@LCL\nD=M\n' + self.constants['push_to_stack'] + '\n'
        asm += '@ARG\nD=M\n' + self.constants['push_to_stack'] + '\n'
        asm += '@THIS\nD=M\n' + self.constants['push_to_stack'] + '\n'
        asm += '@THAT\nD=M\n' + self.constants['push_to_stack'] + '\n'

        # reposition ARG
        asm += f'@SP\nD=M\n@5\nD=D-A\n@{num_args}\nD=D-A\n@ARG\nM=D\n'

        # reposition LCL
        asm += '@SP\nD=M\n@LCL\nM=D\n'

        # goto function
        asm += self.Goto(function_name) + '\n'

        # declare return address label
        asm += self.Label(f'RETURN_ADDRESS{label_counter - 1}') + '\n'

        return asm

    def WriteReturn(self):
        """
        Function that handles the return from a function call in the VM.
    
        Parameters:
            None
    
        Returns:
            str - The assembly code for the return operation.
        """
        # FRAME = LCL
        asm = '@LCL\nD=M\n@R13\nM=D\n'  # R13 = FRAME

        # RET = *(FRAME - 5)
        asm += '@5\nA=D-A\nD=M\n@R14\nM=D\n'  # R14 = RET

        # *ARG = pop()
        asm += '@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n'

        # SP = ARG + 1
        asm += '@ARG\nD=M+1\n@SP\nM=D\n'

        # THAT = *(FRAME - 1)
        asm += '@R13\nAM=M-1\nD=M\n@THAT\nM=D\n'

        # THIS = *(FRAME - 2)
        asm += '@R13\nAM=M-1\nD=M\n@THIS\nM=D\n'

        # ARG = *(FRAME - 3)
        asm += '@R13\nAM=M-1\nD=M\n@ARG\nM=D\n'

        # LCL = *(FRAME - 4)
        asm += '@R13\nAM=M-1\nD=M\n@LCL\nM=D\n'

        # goto RET
        asm += '@R14\nA=M\n0;JMP\n'

        return asm