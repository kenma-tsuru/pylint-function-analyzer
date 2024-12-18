import re
from collections import defaultdict
from typing import Dict, List

from pylint.message import Message
from pylint.reporters.text import TextReporter
from pylint.reporters.ureports.nodes import Section


class FunctionReporter(TextReporter):
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
            self.issues[f"{msg.abspath} : {function_name}"].append(f"({msg.msg_id}) {msg.msg}")
            
    def display_reports(self, layout: Section):
        print("\nFunction Analysis Report")
        print("=" * 80)
        for function_name in sorted(self.issues.keys()):
            print(f"{function_name}")
            for issue in self.issues[function_name]:
                print(f"  {issue}")
        print("=" * 80)