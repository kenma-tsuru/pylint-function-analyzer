import sys
from typing import Dict, List

from pylint.lint import Run

from .reporter import FunctionReporter


def analyze_files(filepaths) -> List[Dict[str, List[str]]]:
    reporter = FunctionReporter()
    result = Run(
        [
            *filepaths,
            "--load-plugins=pylint_function_analyzer",
            "--output-format=function-reporter",
        ],
        reporter=reporter,
        exit=False
    )
    return result.linter.reporter.issues

def main():
    if len(sys.argv) < 2:
        print("Usage: analyze-functions <python_file1> [python_file2 ...]")
        sys.exit(1)

    result = analyze_files(sys.argv[1:])
    print(result)


if __name__ == "__main__":
    main()
