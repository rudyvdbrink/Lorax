from pathlib import Path
import pathspec

DEFAULT_IGNORE_PATTERNS = [
    # VCS
    ".git/",
    ".hg/",
    ".svn/",
    # Python
    ".venv/",
    "venv/",
    "__pycache__/",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".mypy_cache/",
    ".pytest_cache/",
    ".ruff_cache/",
    "*.egg-info/",
    # JS / TS / web
    "node_modules/",
    ".next/",
    "dist/",
    "build/",
    ".parcel-cache/",
    # Common tooling / IDE
    ".idea/",
    ".vscode/",
    ".DS_Store",
]


class Lorax:
    """
    A class to generate and display a directory tree representation of a given root directory.

    The Lorax class provides functionality to recursively traverse a directory structure,
    filter out files and directories based on ignore patterns, and generate a visual
    representation of the directory tree.

    Attributes:
        root (Path): The root directory from which the tree is built.
        ignore_patterns (list[str]): A list of patterns to ignore during traversal.
        _spec (pathspec.PathSpec): A compiled specification for matching ignore patterns.

    Methods:
        build_tree() -> str:
            Constructs and returns a string representation of the directory tree.

        speak() -> None:
            Prints the directory tree representation to the console.
    """
    def __init__(self, root: Path | str = ".",
                 ignore_patterns: list[str] | None = None) -> None:
        self.root = Path(root).resolve()
        self.ignore_patterns = (
            DEFAULT_IGNORE_PATTERNS if ignore_patterns is None else ignore_patterns
        )
        self._spec = pathspec.PathSpec.from_lines("gitwildmatch", self.ignore_patterns)

    def build_tree(self) -> str:
        """Return a directory tree representation for `self.root`."""
        root = self.root
        spec = self._spec
        lines: list[str] = [f"{root.name}/"]

        def _walk(dir_path: Path, prefix: str = "") -> None:
            entries: list[Path] = []
            for p in dir_path.iterdir():
                rel = p.relative_to(root)
                rel_str = str(rel)
                # Append "/" for directories so "*.egg-info/" and ".git/" match the directory itself
                if p.is_dir():
                    rel_str = rel_str.rstrip("/") + "/"
                if spec.match_file(rel_str):
                    continue
                entries.append(p)

            entries.sort(key=lambda p: (p.is_file(), p.name.lower()))

            for i, entry in enumerate(entries):
                connector = "└── " if i == len(entries) - 1 else "├── "
                line = f"{prefix}{connector}{entry.name}"
                if entry.is_dir():
                    line += "/"
                lines.append(line)
                if entry.is_dir():
                    child_prefix = prefix + (
                        "    " if i == len(entries) - 1 else "│   "
                    )
                    _walk(entry, child_prefix)

        _walk(root)
        return "\n".join(lines)

    def speak(self) -> None:
        """Build and print the directory tree."""
        print(self.build_tree())


if __name__ == "__main__":
    # Example usage: run from project root
    Lorax(root='C:/DATA/llmlynx/').speak()
    