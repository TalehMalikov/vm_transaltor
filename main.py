from vm_translator.vm_translator import VMTranslator

if __name__ == '__main__':
    test_files = [
        'data/part1/StackArithmetic/SimpleAdd/SimpleAdd.vm',
        'data/part1/StackArithmetic/StackTest/StackTest.vm',
        'data/part1/MemoryAccess/BasicTest/BasicTest.vm',
        'data/part1/MemoryAccess/PointerTest/PointerTest.vm',
        'data/part1/MemoryAccess/StaticTest/StaticTest.vm',
    ]
    
    for f in test_files:
        print(f"Translating {f}...")
        translator = VMTranslator(f)
        translator.translate()
        print(f"Done!")