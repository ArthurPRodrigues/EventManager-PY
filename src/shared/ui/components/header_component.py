from typing import Any

import FreeSimpleGUI as sg

from shared.ui.styles import BUTTON_SIZES, COLORS, FONTS


class HeaderComponent:
    def __init__(
        self,
        back_button: bool = True,
        extra_buttons: list[dict[str, Any]] | None = None,
    ):
        self.back_button = back_button
        self.buttons = []
        if self.back_button:
            self.buttons.append({
                "text": "Back",
                "font": FONTS["BUTTON"],
                "key": "-BACK-",
                "size": BUTTON_SIZES["EXTRA_SMALL"],
                "button_color": (COLORS["white"], COLORS["error"]),
            })

        if extra_buttons:
            self.buttons.extend(extra_buttons)

    def create_layout(self):
        if not self.buttons:
            return [[]]

        return [
            self._build_button_row(),
            [sg.HSep(color=COLORS["primary_lighter"], pad=((0, 0), (5, 0)))],
        ]

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

    # TODO: Define fallback values for optional button config keys
    def _create_button(self, btn_config: dict[str, Any]) -> sg.Button:
        return sg.Button(
            btn_config["text"],
            font=btn_config.get("font", FONTS["BUTTON"]),
            key=btn_config["key"],
            size=btn_config.get("size", BUTTON_SIZES["SMALL"]),
            button_color=btn_config.get("button_color"),
            pad=btn_config.get("pad", (5, 5)),
        )
