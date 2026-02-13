from vm_translator.vm_translator import VMTranslator

if __name__ == '__main__':
    test_files = [
        'data/StackArithmetic/SimpleAdd/SimpleAdd.vm',
        'data/StackArithmetic/StackTest/StackTest.vm',
        'data/MemoryAccess/BasicTest/BasicTest.vm',
        'data/MemoryAccess/PointerTest/PointerTest.vm',
        'data/MemoryAccess/StaticTest/StaticTest.vm',
    ]
    
    for f in test_files:
        print(f"Translating {f}...")
        translator = VMTranslator(f)
        translator.translate()
        print(f"Done!")