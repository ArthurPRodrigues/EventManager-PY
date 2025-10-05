from typing import Any

import FreeSimpleGUI as sg

from shared.ui.styles import FONTS


class FilterRadioRowComponent:
    def __init__(
        self,
        filters: list[dict[str, Any]] | None = None,
    ):
        self.filters = filters
        self.filter_keys: list[str] = []

    def create_layout(self):
        if not self.filters:
            return [[]]

        self.filter_keys = []

        layout = [self._build_filter_radio_row()]

        return layout

    def _build_filter_radio_row(self) -> list[list[sg.Radio]]:
        row = []
        for index, filter_config in enumerate(self.filters):
            row.append(self._create_filter_radio(filter_config, index))
        return row

    def _create_filter_radio(
        self, filter_config: dict[str, Any], index: int
    ) -> sg.Radio:
        key = self.generate_filter_key(filter_config, index)
        self.filter_keys.append(key)

        return sg.Radio(
            filter_config["text"],
            font=filter_config.get("font", FONTS["RADIO_BUTTON"]),
            circle_color=filter_config.get("circle_color"),
            key=key,
            group_id=filter_config.get("group_id", "default"),
            default=filter_config.get("default"),
            pad=filter_config.get("pad", (5, 10)),
            metadata=filter_config.get("filter_value"),
            enable_events=True,
        )

    def generate_filter_key(self, filter_config: dict[str, Any], index: int) -> str:
        group_id = filter_config.get("group_id", "default")
        return f"-FILTER-{group_id}-{index}-"
