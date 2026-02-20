from vm_translator.translations import Translations

class CodeWriter:
    def __init__(self, filename):
        self.file = open(filename, 'w')
        self.label_counter = 0  # for unique labels in eq, gt, lt
        self.translations = Translations()

    def write_init(self):
        asm = '@256\nD=A\n@SP\nM=D\n'
        asm += self.translations.WriteCall('Sys.init', 0)
        self.file.write(asm + '\n')

    def write_push(self, segment, index):
        asm = self.translations.Push(segment, index)
        self.file.write(asm + '\n')

    def write_pop(self, segment, index):
        asm = self.translations.Pop(segment, index)
        self.file.write(asm + '\n')

    def write_arithmetic(self, cmd):
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
        asm = self.translations.Label(label)
        self.file.write(asm + '\n')
    
    def write_goto(self, label):
        asm = self.translations.Goto(label)
        self.file.write(asm + '\n')
    
    def write_if(self, label):
        asm = self.translations.IfGoto(label)
        self.file.write(asm + '\n')

    def write_function(self, function_name, num_locals):
        asm = self.translations.WriteFunction(function_name, num_locals)
        self.file.write(asm + '\n')
    
    def write_call(self, function_name, num_args):
        asm = self.translations.WriteCall(function_name, num_args)
        self.file.write(asm + '\n')

    def write_return(self):
        asm = self.translations.WriteReturn()
        self.file.write(asm + '\n')

    def close(self):
        self.file.write('(END)\n@END\n0;JMP\n')
        self.file.close()