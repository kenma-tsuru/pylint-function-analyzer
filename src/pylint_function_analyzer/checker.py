from dataclasses import dataclass

from astroid import nodes
from pylint.checkers import BaseChecker


class FunctionAnalyzerChecker(BaseChecker):
    name = "function-analyzer"
    priority = -1

    msgs = {
        "C9001": (
            "Function '%s' has too many arguments (%s/%s)",
            "custom-too-many-function-args",
            "Function has more arguments than allowed",
        ),
        "C9002": (
            "Function '%s' is too complex (%s/%s)",
            "custom-function-too-complex",
            "Function has too high cyclomatic complexity",
        ),
        "C9003": (
            "Function '%s' has too many local variables (%s/%s)",
            "custom-too-many-locals",
            "Function has too many local variables",
        ),
        "C9004": (
            "Function '%s' has too many nested loops (%s/%s)",
            "custom-too-many-nested-loops",
            "Function has too many nested loops",
        ),
        "C9005": (
            "Function '%s' has too many statements (%s/%s)",
            "custom-too-many-statements",
            "Function has too many statements",
        ),
        "C9006": (
            "Function '%s' has too many lines (%s/%s)",
            "custom-too-many-lines",
            "Function has too many lines",
        ),
    }

    options = (
        (
            "max-function-args",
            {
                "default": 4,
                "type": "int",
                "metavar": "<int>",
                "help": "Maximum number of arguments for a function",
            },
        ),
        (
            "max-function-complexity",
            {
                "default": 3,
                "type": "int",
                "metavar": "<int>",
                "help": "Maximum cyclomatic complexity for a function",
            },
        ),
        (
            "max-local-vars",
            {
                "default": 5,
                "type": "int",
                "metavar": "<int>",
                "help": "Maximum number of local variables in a function",
            },
        ),
        (
            "max-nested-depth",
            {
                "default": 2,
                "type": "int",
                "metavar": "<int>",
                "help": "Maximum nested depth for a function",
            },
        ),
        (
            "max-statements",
            {
                "default": 20,
                "type": "int",
                "metavar": "<int>",
                "help": "Maximum number of statements in a function",
            },
        ),
        (
            "max-lines",
            {
                "default": 50,
                "type": "int",
                "metavar": "<int>",
                "help": "Maximum number of lines in a function",
            },
        ),
    )

    def __init__(self, linter=None):
        super().__init__(linter)
        

    def visit_functiondef(self, node: nodes.FunctionDef):
        # check number of arguments
        if len(node.args.args) > self.linter.config.max_function_args:
            self.add_message("C9001", node=node, args=(node.name, len(node.args.args), self.linter.config.max_function_args))

        # check complexity
        if self._compute_complexity(node) > self.linter.config.max_function_complexity:
            self.add_message("C9002", node=node, args=(node.name, self._compute_complexity(node), self.linter.config.max_function_complexity))

        # check number of local variables
        if len(node.locals) > self.linter.config.max_local_vars:
            self.add_message("C9003", node=node, args=(node.name, len(node.locals), self.linter.config.max_local_vars))
        
        # check nested depth
        if self._compute_nested_depth(node) > self.linter.config.max_nested_depth:
            self.add_message("C9004", node=node, args=(node.name, self._compute_nested_depth(node), self.linter.config.max_nested_depth))
        
        # check number of statements
        if len(node.body) > self.linter.config.max_statements:
            self.add_message("C9005", node=node, args=(node.name, len(node.body), self.linter.config.max_statements))
        
        # check number of lines
        if self._compute_code_lines(node) > self.linter.config.max_lines:
            self.add_message("C9006", node=node, args=(node.name, self._compute_code_lines(node), self.linter.config.max_lines))

    def _compute_complexity(self, node):
        complexity = 1
        for child in node.nodes_of_class((nodes.If, nodes.While, nodes.For)):
            complexity += 1
        return complexity

    def _compute_nested_depth(self, node, current_depth=0):
        max_depth = current_depth
        for child in node.get_children():
            if isinstance(child, (nodes.If, nodes.For, nodes.While)):
                child_depth = self._compute_nested_depth(child, current_depth + 1)
                max_depth = max(max_depth, child_depth)
            else:
                child_depth = self._compute_nested_depth(child, current_depth)
                max_depth = max(max_depth, child_depth)
        return max_depth

    def _compute_code_lines(self, node: nodes.FunctionDef):
        """Compute the number of code lines in a function, excluding docstring."""
        # Get total lines
        total_lines = node.tolineno - node.fromlineno + 1
        
        # Subtract docstring lines if present
        if node.doc_node:
            doc_node = node.doc_node
            doc_lines = doc_node.tolineno - doc_node.fromlineno + 1
            total_lines -= doc_lines
        
        return total_lines