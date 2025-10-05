from collections.abc import Callable
from typing import Any

import FreeSimpleGUI as sg

from shared.ui.components.filter_radio_row_component import FilterRadioRowComponent
from shared.ui.styles import BUTTON_SIZES, COLORS, FONTS, LABEL_SIZES


class TableComponent:
    def __init__(
        self,
        headers: list[str],
        data_callback: Callable[..., dict[str, Any]],
        pad: Any | None = (10, 20),
        key: str = "-TABLE-",
        items_per_page: int = 10,
        has_hidden_id_column: bool = False,
        filters: list[dict[str, Any]] | None = None,
    ):
        self.headers = headers
        self.data_callback = data_callback
        self.pad = pad
        self.key = key
        self.items_per_page = items_per_page
        self.has_hidden_id_column = has_hidden_id_column
        self.filters = filters
        self.current_page = 1
        self.total_items = 0
        self.total_pages = 1
        self.data = []

        self.prev_key = f"{key}_PREV"
        self.next_key = f"{key}_NEXT"
        self.page_info_key = f"{key}_PAGE_INFO"
        self.total_items_key = f"{key}_TOTAL"
        self.filter_component = FilterRadioRowComponent(self.filters)

        self._load_data()

    def create_layout(self):
        visible_columns = None
        if self.has_hidden_id_column:
            visible_columns = [False] + [True] * (len(self.headers) - 1)

        pagination_layout = [
            [
                sg.Button(
                    "< Previous",
                    key=self.prev_key,
                    disabled=(self.current_page <= 1),
                    size=BUTTON_SIZES["SMALL"],
                    font=FONTS["PAGINATION_BUTTON"],
                ),
                sg.Text(
                    f"Page {self.current_page}/{self.total_pages}",
                    key=self.page_info_key,
                    size=LABEL_SIZES["DEFAULT"],
                    justification="center",
                    font=FONTS["PAGINATION_INFO"],
                ),
                sg.Button(
                    "Next >",
                    key=self.next_key,
                    disabled=(self.current_page >= self.total_pages),
                    size=BUTTON_SIZES["SMALL"],
                    font=FONTS["PAGINATION_BUTTON"],
                ),
                sg.Push(),
                sg.Text(
                    f"Total: {self.total_items}",
                    key=self.total_items_key,
                    size=LABEL_SIZES["DEFAULT"],
                    justification="right",
                    font=FONTS["PAGINATION_INFO"],
                ),
            ]
        ]

        table_layout = [
            *self.filter_component.create_layout(),
            [
                sg.Table(
                    values=self.data,
                    headings=self.headers,
                    pad=((0, 0), (0, 20)),
                    max_col_width=35,
                    auto_size_columns=True,
                    justification="center",
                    num_rows=self.items_per_page,
                    alternating_row_color=COLORS["primary_lighter"],
                    key=self.key,
                    selected_row_colors=f"{COLORS['white']} on {COLORS['secondary_darker']}",
                    enable_events=True,
                    expand_x=True,
                    enable_click_events=True,
                    visible_column_map=visible_columns,
                    select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                    font=FONTS["MONOSPACED"],
                    header_font=FONTS["TABLE_HEADER"],
                    header_border_width=0,
                    header_relief="flat",
                    hide_vertical_scroll=True,
                    border_width=0,
                )
            ],
            *pagination_layout,
        ]

        layout = [
            [sg.Column([*table_layout], expand_x=True, pad=self.pad)],
        ]

        return layout

    def _load_data(self, window: sg.Window | None = None):
        try:
            filter_value = None

            if self.filters:
                is_window_available = window is not None

                if is_window_available:
                    filter_value = self._get_selected_filter_value(window)
                else:
                    filter_value = self._get_default_filter_value()

            if filter_value is not None:
                result = self.data_callback(
                    self.current_page, self.items_per_page, filter_value
                )
            else:
                result = self.data_callback(self.current_page, self.items_per_page)

            self.data = result.get("data", [])
            self.total_items = result.get("total", 0)
            self.total_pages = max(
                1, (self.total_items + self.items_per_page - 1) // self.items_per_page
            )
        # TODO: Discover how to throw and handle errors in the parent component
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            self.data = []
            self.total_items = 0
            self.total_pages = 1

    def handle_event(self, event: str, window: sg.Window) -> bool:
        if event == self.prev_key and self.current_page > 1:
            self.current_page -= 1
            self._load_data(window)
            self._update_ui(window)
            return True

        elif event == self.next_key and self.current_page < self.total_pages:
            self.current_page += 1
            self._load_data(window)
            self._update_ui(window)
            return True

        if self.filters:
            if event in self.filter_component.filter_keys:
                self.current_page = 1
                self._load_data(window)
                self._update_ui(window)
                return True

        return False

    def _update_ui(self, window: sg.Window):
        """Atualiza a interface após mudança de página"""
        # Atualiza a tabela com os novos dados
        window[self.key].update(values=self.data)

        # Atualiza contador total
        window[self.total_items_key].update(f"Total: {self.total_items}")

        # Atualiza informação da página
        window[self.page_info_key].update(
            f"Page {self.current_page}/{self.total_pages}"
        )

        # Atualiza estado dos botões
        window[self.prev_key].update(disabled=(self.current_page <= 1))
        window[self.next_key].update(disabled=(self.current_page >= self.total_pages))

    def refresh(self, window: sg.Window):
        self._load_data(window)
        self._update_ui(window)

    def _get_selected_filter_value(self, window: sg.Window) -> Any:
        keys = self.filter_component.filter_keys
        for key in keys:
            element = window[key]
            if element.get():
                return element.metadata

        return None

    def _get_default_filter_value(self) -> Any:
        for filter_config in self.filters:
            if filter_config.get("default"):
                return filter_config.get("filter_value")

        return None

    def get_selected_row_data(self, window: sg.Window) -> list[Any]:
        try:
            selected_rows = window[self.key].get()
            if selected_rows and len(selected_rows) > 0:
                selected_index = selected_rows[0]
                if 0 <= selected_index < len(self.data):
                    return self.data[selected_index]
        except Exception:
            pass
        return []
