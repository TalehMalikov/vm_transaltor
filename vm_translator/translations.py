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
        return '@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M'
    
    def Sub(self):
        return '@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D'
    
    def Neg(self):
        return '@SP\nA=M-1\nM=-M'
    
    def Compare(self, jump, label_num):
        return f'@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@TRUE{label_num}\nD;{jump}\n@SP\nA=M-1\nM=0\n@END{label_num}\n0;JMP\n(TRUE{label_num})\n@SP\nA=M-1\nM=-1\n(END{label_num})'
    
    def And(self):
        return '@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M'
    
    def Or(self):
        return '@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M'
    
    def Not(self):
        return '@SP\nA=M-1\nM=!M'
    
    def Push(self, segment, index):
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
            return f'@Static.{index}\nD=M\n{self.constants["push_to_stack"]}'
        return ''  # for segments that don't support push
    
    def Pop(self, segment, index):
        if segment in ['local', 'argument', 'this', 'that']:
            return f'@{index}\nD=A\n@{self.constants["seg_ptrs"][segment]}\nD=M+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D'
        elif segment == 'temp':
            return f'@{index}\nD=A\n@5\nD=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D'
        elif segment == 'pointer':
            ptrs = {'0': 'THIS', '1': 'THAT'}
            return f'@SP\nAM=M-1\nD=M\n@{ptrs[index]}\nM=D'
        elif segment == 'static':
            return f'@SP\nAM=M-1\nD=M\n@Static.{index}\nM=D'
        return ''  # for segments that don't support pop
    
    def Label(self, label):
        return f'({label})'

    def Goto(self, label):
        return f'@{label}\n0;JMP'
    
    def IfGoto(self, label):
        return f'@SP\nAM=M-1\nD=M\n@{label}\nD;JNE'
    
    def WriteFunction(self, function_name, num_locals):
        asm = f'({function_name})\n'
        for i in range(int(num_locals)):
            asm += self.Push('constant', '0') + '\n'
        return asm
    
    def WriteCall(self, function_name, num_args):
        #push return address
        asm = f'@RETURN_ADDRESS{self.label_counter}\nD=A\n{self.constants["push_to_stack"]}\n'
        self.label_counter += 1

        # push LCL, ARG, THIS, THAT
        asm += '@LCL\nD=M\n' + self.constants['push_to_stack'] + '\n'
        asm += '@ARG\nD=M\n' + self.constants['push_to_stack'] + '\n'
        asm += '@THIS\nD=M\n' + self.constants['push_to_stack'] + '\n'
        asm += '@THAT\nD=M\n' + self.constants['push_to_stack'] + '\n'

        # reposition ARG
        asm += '@SP\nD=M\n@5\nD=D-A\n@{num_args}\nD=D-A\n@ARG\nM=D\n'

        # reposition LCL
        asm += '@SP\nD=M\n@LCL\nM=D\n'

        # goto function
        asm += self.Goto(function_name) + '\n'

        # declare return address label
        asm += self.Label(f'RETURN_ADDRESS{self.label_counter - 1}') + '\n'

        return asm

    def WriteReturn(self):
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
