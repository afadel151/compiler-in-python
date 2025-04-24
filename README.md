# Mini Compiler Project

This is a Python-based mini compiler that implements lexical analysis, parsing, and interpretation of a simple programming language with both English and French keywords.

## Prerequisites

- Python 3.6 or higher
- Graphviz (for visualization)
  - Ubuntu/Debian: `sudo apt-get install graphviz`
  - macOS: `brew install graphviz`
  - Windows: Download from [Graphviz official site](https://graphviz.org/download/)

## Setup Instructions

### 1. Clone the repository (if applicable)
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create and activate a virtual environment

#### On Linux/macOS:
```bash
python -m venv venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Project Structure
```
.
├── AST.py             # Abstract Syntax Tree implementation
├── lex.py             # Lexical analyzer
├── parser.py          # Syntax parser
├── interpreter.py     # Code interpreter/executor
├── threader.py        # Control flow visualizer
├── requirements.txt   # Dependencies
└── examples/          # Example programs (create this folder)
```

## Running the Compiler

### 1. Create an example program
Create a file named `example.txt` with your program code. Example:
```text
main() {
    x = 5;
    print(x);
}
```

### 2. Run the compiler (choose one method)

#### Method 1: Just parse and execute
```bash
python interpreter.py example.txt
```

#### Method 2: Parse and visualize the AST
```bash
python threader.py example.txt
```
This will generate a visualization file `ABR/prog.png`

#### Method 3: Run just the lexer
```bash
python lex.py example.txt
```

#### Method 4: Run just the parser
```bash
python parser.py example.txt
```

## Example Programs

Create test programs in the `examples/` folder. Here are some sample programs you can try:

1. **Simple calculation** (`examples/calc.txt`):
```text
main() {
    a = 10;
    b = 20;
    print(a + b);
}
```

2. **Conditional statement** (`examples/if.txt`):
```text
main() {
    x = 15;
    if (x > 10) {
        print("x is greater than 10");
    }
}
```

3. **While loop** (`examples/while.txt`):
```text
main() {
    i = 0;
    while (i < 5) {
        print(i);
        i = i + 1;
    }
}
```

## Language Features Supported

- Variables and assignment
- Arithmetic operations (+, -, *, /)
- Comparison operations (>, <, ==, !=, etc.)
- Logical operations (&&, ||, !)
- Control structures:
  - if/else (both English and French: if/si, then/alors, else/sinon)
  - while loops (while/tantque)
- I/O operations:
  - print/ecrire
  - read/lire
- Function declarations and calls

## Troubleshooting

1. **Graphviz not found**:
   - Ensure Graphviz is installed on your system
   - Add Graphviz to your system PATH if needed

2. **Module not found errors**:
   - Ensure your virtual environment is activated
   - Run `pip install -r requirements.txt` again

3. **Syntax errors in your program**:
   - Check the line number reported in the error message
   - Verify you're using supported keywords and syntax

## License

This project is provided for educational purposes. Feel free to modify and extend it for your needs.

---

You can copy this content into a `README.md` file in your project directory. The Markdown formatting will render nicely on GitHub or other platforms that support