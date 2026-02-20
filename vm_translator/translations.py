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