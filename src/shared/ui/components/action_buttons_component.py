from typing import Any

import FreeSimpleGUI as sg


class ActionButtonsComponent:
    def __init__(self, buttons: list[dict[str, Any]]):
        self.buttons = buttons

    def create_layout(self):
        return [[sg.VPush()], self._build_button_row()]

    def _build_button_row(self):
        if len(self.buttons) == 1:
            return [sg.Push(), self._create_button(self.buttons[0]), sg.Push()]
        else:
            row = []
            for btn in self.buttons:
                row.append(self._create_button(btn))
                row.append(sg.Push())
            if row:
                row.pop()  # Remove the last sg.Push() as it's not needed
            return row

    def _create_button(self, btn: dict[str, Any]):
        return sg.Button(btn["text"], key=btn["key"], size=btn.get("size", (10, 1)))
