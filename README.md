# Lorax

Lorax speaks for the trees: it prints a clean directory tree for your project, excluding heavy / generated directories like virtual environments, build artifacts, and caches — useful for project overviews in a `README.md`.

## Installation

```bash
pip install lorax-tree
```

## Usage

```python
from lorax import Lorax

lorax = Lorax(".")
lorax.speak()
```

This prints a tree for the current working directory, for example:

```text
Lorax/
├── .git/
├── .venv/
├── src/
│   └── lorax/
│       ├── __init__.py
│       ├── __main__.py
│       └── lorax.py
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

