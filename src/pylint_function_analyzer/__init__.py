from pylint.lint import PyLinter

from .checker import FunctionAnalyzerChecker
from .reporter import FunctionReporter


def register(linter: PyLinter):
    """Register the checker and reporter."""
    linter.register_checker(FunctionAnalyzerChecker(linter))
    linter.register_reporter(FunctionReporter)
