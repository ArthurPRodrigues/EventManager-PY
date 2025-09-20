from typing import Any, Dict, List

import FreeSimpleGUI as sg


class ActionButtonsComponent:
    def __init__(self, buttons: List[Dict[str, Any]]):
        self.buttons = buttons

    def create_layout(self):
        return [
            [
                sg.Button(btn["text"], key=btn["key"], size=btn.get("size", (10, 1)))
                for btn in self.buttons
            ]
        ]
