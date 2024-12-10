import re
from pylint.reporters import BaseReporter
from pylint.message import Message
from pylint.reporters.ureports.nodes import Section
from collections import defaultdict
from typing import Dict, List


class FunctionReporter(BaseReporter):
    name = 'function-reporter'

    def __init__(self):
        super().__init__()
        self.issues: Dict[str, List[str]] = defaultdict(list)

    def handle_message(self, msg: Message):
        if not msg.msg_id.startswith('C90'):
            return
        match = re.match(r"Function '([^']+)'", msg.msg)
        if match:
            function_name = match.group(1)
            self.issues[f"{msg.abspath} : {function_name}"].append(msg.msg)

    def display_reports(self, layout: Section):
        print("\nFunction Analysis Report")
        print("=" * 80)
        for function_name in self.issues:
            print(f"{function_name}")
            for issue in self.issues[function_name]:
                print(f"  {issue}")
        print("=" * 80)