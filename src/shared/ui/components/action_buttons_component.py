from typing import Any

import FreeSimpleGUI as sg

from shared.ui.styles import BUTTON_SIZES, FONTS


class ActionButtonsComponent:
    def __init__(self, buttons: list[dict[str, Any]]):
        self.buttons = buttons

    def create_layout(self):
        if not self.buttons:
            return [[]]

        layout = [self._build_button_row()]
        layout.insert(0, [sg.VPush()])
        return layout

    def _build_button_row(self) -> list[sg.Element]:
        row = []
        for btn_config in self.buttons:
            row.append(self._create_button(btn_config))
            row.append(sg.Push())
        if row:
            row.pop()
        return row

    # TODO: Define fallback values for optional button config keys
    def _create_button(self, btn_config: dict[str, Any]) -> sg.Button:
        return sg.Button(
            btn_config["text"],
            font=btn_config.get("font", FONTS["BUTTON"]),
            key=btn_config["key"],
            size=btn_config.get("size", BUTTON_SIZES["SMALL"]),
            button_color=btn_config.get("button_color"),
            pad=btn_config.get("pad", (10, 15)),
        )
