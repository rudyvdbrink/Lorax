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
            entries = sorted(
                [
                    p
                    for p in dir_path.iterdir()
                    if not spec.match_file(str(p.relative_to(root)))
                ],
                key=lambda p: (p.is_file(), p.name.lower()),
            )

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
    Lorax().speak()
    