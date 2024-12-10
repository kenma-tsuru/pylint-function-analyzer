from pylint.lint import Run
import sys
from .reporter import FunctionReporter


def analyze_file(filepath):
    reporter = FunctionReporter()
    Run(
        [
            filepath,
            "--load-plugins=pylint_function_analyzer",
            "--output-format=function-reporter",
        ],
        reporter=reporter,
        exit=False,
    )


def main():
    if len(sys.argv) != 2:
        print("Usage: analyze-functions <python_file>")
        sys.exit(1)

    analyze_file(sys.argv[1])


if __name__ == "__main__":
    main()
