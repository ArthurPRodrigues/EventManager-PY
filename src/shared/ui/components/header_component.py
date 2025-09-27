from typing import Any

import FreeSimpleGUI as sg


class HeaderComponent:
    def __init__(
        self,
        back_button: bool = True,
        extra_buttons: list[dict[str, Any]] | None = None,
    ):
        self.back_button = back_button
        self.buttons = []
        if self.back_button:
            self.buttons.append({"text": "Back", "key": "-BACK-", "size": (8, 1)})

        if extra_buttons:
            self.buttons.extend(extra_buttons)

    def create_layout(self):
        if not self.buttons:
            return [[]]

        return [self._build_button_row()]

    def _build_button_row(self) -> list[sg.Element]:
        if self.back_button:
            row = [self._create_button(self.buttons[0]), sg.Push()]
            for btn_config in self.buttons[1:]:
                row.append(self._create_button(btn_config))
            return row
        else:
            return self._build_button_space_between(self.buttons)

    def _build_button_space_between(
        self, buttons: list[dict[str, Any]] | None = None
    ) -> list[sg.Element]:
        if buttons is None:
            buttons = self.buttons
        row = []
        for btn_config in buttons:
            row.append(self._create_button(btn_config))
            row.append(sg.Push())
        if row:
            row.pop()
        return row

    def _create_button(self, btn_config: dict[str, Any]) -> sg.Button:
        return sg.Button(
            btn_config["text"],
            key=btn_config["key"],
            size=btn_config.get("size"),
        )
