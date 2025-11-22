from pathlib import Path
from .lorax import Lorax


def main() -> None:
    # Default to current working directory
    Lorax(Path.cwd()).speak()


if __name__ == "__main__":
    main()