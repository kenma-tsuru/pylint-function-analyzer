from .checker import FunctionAnalyzerChecker
from .reporter import FunctionReporter
from pylint.lint import PyLinter

def register(linter: PyLinter):
    """Register the checker and reporter."""
    linter.register_checker(FunctionAnalyzerChecker(linter))
    linter.register_reporter(FunctionReporter)
