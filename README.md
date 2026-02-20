# VM Translator – Projects 7 & 8 (Nand2Tetris)

A Python-based VM Translator that converts Hack VM language (`.vm`) into Hack Assembly (`.asm`), built as part of the Nand2Tetris course (Project 8).

---

## Project Structure

```
malikovTalehProject8/
├── main.py                  # Entry point — runs the translator on test files
├── data/                    # Input .vm files and output .asm files
│   ├── part1/
│   │   ├── StackArithmetic/
│   │   │   ├── SimpleAdd/
│   │   │   └── StackTest/
│   │   └── MemoryAccess/
│   │       ├── BasicTest/
│   │       ├── PointerTest/
│   │       └── StaticTest/
│   └── part2/
│       ├── ProgramFlow/
│       │   ├── BasicLoop/
│       │   └── FibonacciSeries/
│       └── FunctionCalls/
│           ├── SimpleFunction/
│           ├── NestedCall/
│           ├── FibonacciElement/
│           └── StaticsTest/
├── vm_translator/           # Core translation package
│   ├── __init__.py
│   ├── vm_translator.py     # VMTranslator — orchestrates the translation
│   ├── parser.py            # Parser — reads and parses VM commands
│   ├── code_writer.py       # CodeWriter — generates Assembly output
│   └── translations.py      # Translation helpers / mappings
├── pyproject.toml
└── README.md
```

---

## How It Works

The translator follows a two-stage pipeline:

1. **Parser** — reads a `.vm` file line by line, strips comments and whitespace, and classifies each command into types: `C_PUSH`, `C_POP`, `C_ARITHMETIC`, `C_LABEL`, `C_GOTO`, `C_IF`, `C_FUNCTION`, `C_CALL`, or `C_RETURN`.

2. **CodeWriter** — takes parsed commands and writes the corresponding Hack Assembly instructions to an `.asm` output file.

The `VMTranslator` class ties these two together. It can handle both a single `.vm` file and an entire folder of `.vm` files, combining them into one `.asm` output.

---

## Supported VM Commands

### Stack Arithmetic
| Command | Description |
|---------|-------------|
| `add` | Pops two values, pushes their sum |
| `sub` | Pops two values, pushes their difference |
| `neg` | Negates the top value |
| `eq` | Pushes `true` if top two are equal |
| `gt` | Pushes `true` if second > top |
| `lt` | Pushes `true` if second < top |
| `and` | Bitwise AND of top two values |
| `or` | Bitwise OR of top two values |
| `not` | Bitwise NOT of top value |

### Memory Access
| Command | Description |
|---------|-------------|
| `push <segment> <index>` | Pushes value from segment onto the stack |
| `pop <segment> <index>` | Pops top of stack into segment |

### Program Flow
| Command | Description |
|---------|-------------|
| `label <label>` | Declares a label in the current function |
| `goto <label>` | Unconditional jump to label |
| `if-goto <label>` | Pops top of stack; jumps to label if non-zero |

### Function Commands
| Command | Description |
|---------|-------------|
| `function <name> <nVars>` | Declares a function, initializes nVars locals to 0 |
| `call <name> <nArgs>` | Calls a function with nArgs arguments |
| `return` | Returns from current function to the caller |

### Supported Memory Segments
| Segment | Description |
|---------|-------------|
| `constant` | Virtual segment — push only |
| `local` | Local variables (`LCL`) |
| `argument` | Function arguments (`ARG`) |
| `this` | `THIS` pointer |
| `that` | `THAT` pointer |
| `temp` | Registers `R5–R12` |
| `pointer` | `THIS` (0) or `THAT` (1) |
| `static` | Static variables (file-scoped) |

---

## Usage

Run the translator from the project root:

```bash
python main.py
```

Edit `main.py` to choose which `.vm` files or folders to translate:

```python
test_files = [
    'data/part2/ProgramFlow/BasicLoop/BasicLoop.vm',  # single file
    'data/part2/FunctionCalls/FibonacciElement/',      # folder
]
```

Single `.vm` files produce a corresponding `.asm` file in the same directory. Folders produce a single `.asm` file named after the folder, with bootstrap code prepended.

---

## Bootstrap

When translating a folder, the translator automatically:
1. Sets `SP = 256`
2. Calls `Sys.init` as the program entry point

Single files do not get bootstrap code.

---

## Testing

Use the **CPU Emulator** from the Nand2Tetris software suite to verify output:

1. Load the generated `.asm` file into the CPU Emulator.
2. Load the corresponding `.tst` test script.
3. Run the script — **"Comparison ended successfully"** means the output is correct.

---

## Requirements

- Python 3.x
- No external dependencies

---

## Course

[Nand2Tetris](https://www.nand2tetris.org/) — *Building a Modern Computer from First Principles*  
Projects 7 & 8: Virtual Machine Translator (Parts I & II)

---

## Repository

Source code is available on GitHub:
[https://github.com/TalehMalikov/vm_transaltor](https://github.com/TalehMalikov/vm_transaltor)

```bash
git clone https://github.com/TalehMalikov/vm_transaltor.git
```

---

## Collaboration

This project was developed with the assistance of **Claude** (AI assistant by Anthropic), who helped prepare and update the project documentation and assisted in identifying and debugging issues during the development of the VM translator, particularly around the function calling convention and static variable handling across multiple files.

---

## Weakness

This implementation prioritizes simplicity and correctness over performance. No cycle optimization was done — every operation goes through the stack even when intermediate pushes and pops could be avoided by keeping values in registers directly. 

---

## Author

Taleh Malikov
