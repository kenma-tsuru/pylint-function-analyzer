import sys
from typing import Dict, List

from pylint.lint import Run

from .reporter import FunctionReporter


def analyze_file(filepath) -> List[Dict[str, List[str]]]:
    reporter = FunctionReporter()
    result = Run(
        [
            filepath,
            "--load-plugins=pylint_function_analyzer",
            "--output-format=function-reporter",
        ],
        reporter=reporter,
        exit=False
    )
    return result.linter.reporter.issues

def main():
    if len(sys.argv) != 2:
        print("Usage: analyze-functions <python_file>")
        sys.exit(1)

    analyze_file(sys.argv[1])


if __name__ == "__main__":
    main()
