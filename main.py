from fnmatch import translate

from vm_translator.vm_translator import VMTranslator

if __name__ == '__main__':
    test_files = [
        'data/part1/StackArithmetic/SimpleAdd/SimpleAdd.vm',
        'data/part1/StackArithmetic/StackTest/StackTest.vm',
        'data/part1/MemoryAccess/BasicTest/BasicTest.vm',
        'data/part1/MemoryAccess/PointerTest/PointerTest.vm',
        'data/part1/MemoryAccess/StaticTest/StaticTest.vm',
    ]

    test_files = [
        'data/part2/ProgramFlow/BasicLoop/BasicLoop.vm',
        'data/part2/ProgramFlow/FibonacciSeries/FibonacciSeries.vm',
        'data/part2/FunctionCalls/SimpleFunction/SimpleFunction.vm',
        # these need the FOLDER, not a single file
        'data/part2/FunctionCalls/FibonacciElement/',
        'data/part2/FunctionCalls/NestedCall/',
        'data/part2/FunctionCalls/StaticsTest/',
    ]

    input = [
        'data/part2/ProgramFlow/BasicLoop/BasicLoop.vm',
        'data/part2/ProgramFlow/FibonacciSeries/FibonacciSeries.vm',
        'data/part2/FunctionCalls/SimpleFunction/SimpleFunction.vm',
        # these need the FOLDER, not a single file
        'data/part2/FunctionCalls/FibonacciElement/',
        'data/part2/FunctionCalls/NestedCall/',
        'data/part2/FunctionCalls/StaticsTest/',
    ]

    translator = VMTranslator()
    for f in input:
        if f.endswith('.vm'): #single file
            print(f"Translating file {f}...") 
            translator.write_file(f)

        else: #folder
            print(f"Translating folder {f}...")
            translator.write_folder(f)
        
    print(f"Yayyy!")