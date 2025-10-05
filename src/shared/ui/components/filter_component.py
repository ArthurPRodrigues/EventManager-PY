from typing import Any

import FreeSimpleGUI as sg

from shared.ui.styles import FONTS


class FilterComponent:
    def __init__(
        self,
        filters: list[dict[str, Any]] | None = None,
    ):
        self.filters = filters

    def create_layout(self):
        if not self.filters:
            return [[]]

        layout = [self._build_filter_row()]

        return layout

    def _build_filter_row(self) -> list[Any]:
        row = []
        for filter_config in self.filters:
            row.append(self._create_filter(filter_config))
        return row

    def _create_filter(self, filter_config: dict[str, Any]) -> sg.Radio:
        return sg.Radio(
            filter_config["text"],
            font=filter_config.get("font", FONTS["RADIO_BUTTON"]),
            circle_color=filter_config.get("circle_color"),
            key=filter_config["key"],
            group_id=filter_config.get("group_id", "default"),
            default=filter_config.get("default"),
            pad=filter_config.get("pad", (5, 10)),
        )
