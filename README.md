# VM Translator – Project 7 (Nand2Tetris)

A Python-based VM Translator that converts Hack VM language (`.vm`) into Hack Assembly (`.asm`), built as part of the Nand2Tetris course (Project 7).

---

## Project Structure

```
malikovTalehProject7/
├── main.py                  # Entry point — runs the translator on test files
├── data/                    # Input .vm files and output .asm files
│   ├── StackArithmetic/
│   │   ├── SimpleAdd/
│   │   └── StackTest/
│   └── MemoryAccess/
│       ├── BasicTest/
│       ├── PointerTest/
│       └── StaticTest/
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

1. **Parser** — reads a `.vm` file line by line, strips comments and whitespace, and classifies each command into types: `C_PUSH`, `C_POP`, or `C_ARITHMETIC`.

2. **CodeWriter** — takes parsed commands and writes the corresponding Hack Assembly instructions to an `.asm` output file.

The `VMTranslator` class ties these two together and drives the full translation process.

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

Edit `main.py` to choose which `.vm` files to translate:

```python
test_files = [
    'data/StackArithmetic/SimpleAdd/SimpleAdd.vm',
    'data/MemoryAccess/BasicTest/BasicTest.vm',
    # add more as needed
]
```

Each `.vm` file will produce a corresponding `.asm` file in the same directory.

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
Project 7: Virtual Machine Translator (Part I)

---

## Repository

Source code is available on GitHub:
[https://github.com/TalehMalikov/vm_transaltor](https://github.com/TalehMalikov/vm_transaltor)

```bash
git clone https://github.com/TalehMalikov/vm_transaltor.git
```

---

## Author

Taleh Malikov