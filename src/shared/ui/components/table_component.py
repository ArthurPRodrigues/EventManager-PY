from typing import Any, List

import FreeSimpleGUI as sg


class TableComponent:
    def __init__(self, headers: List[str], data: List[List[Any]], key: str = "-TABLE-"):
        self.headers = headers
        self.data = data
        self.key = key

    def create_layout(self):
        return [
            [
                sg.Table(
                    values=self.data,
                    headings=self.headers,
                    max_col_width=35,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification="left",
                    num_rows=10,
                    alternating_row_color="lightgray",
                    key=self.key,
                    selected_row_colors="red on yellow",
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True,
                )
            ]
        ]

    def update_data(self, new_data: List[List[Any]]):
        self.data = new_data
