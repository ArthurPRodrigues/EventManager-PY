from typing import Any, Callable, Dict, List

import FreeSimpleGUI as sg


class TableComponent:
    def __init__(
        self,
        headers: List[str],
        data_callback: Callable[[int, int], Dict[str, Any]],
        key: str = "-TABLE-",
        items_per_page: int = 10,
        has_hidden_id_column: bool = False,
    ):
        self.headers = headers
        self.data_callback = data_callback
        self.key = key
        self.items_per_page = items_per_page
        self.has_hidden_id_column = has_hidden_id_column
        self.current_page = 1
        self.total_items = 0
        self.total_pages = 1
        self.data = []

        self.prev_key = f"{key}_PREV"
        self.next_key = f"{key}_NEXT"
        self.page_info_key = f"{key}_PAGE_INFO"
        self.total_items_key = f"{key}_TOTAL"

        self._load_data()
    
    def create_layout(self):
        visible_columns = None
        if self.has_hidden_id_column:
            visible_columns = [False] + [True] * (len(self.headers) - 1)

        table_layout = [
            sg.Table(
                values=self.data,
                headings=self.headers,
                max_col_width=35,
                auto_size_columns=True,
                display_row_numbers=False,
                justification="left",
                num_rows=self.items_per_page,
                alternating_row_color="lightgray",
                key=self.key,
                selected_row_colors="red on yellow",
                enable_events=True,
                expand_x=True,
                expand_y=True,
                enable_click_events=True,
                visible_column_map=visible_columns,
                select_mode=sg.TABLE_SELECT_MODE_BROWSE,
            )
        ]

        pagination_layout = [
            sg.Push(),
            sg.Text(f"Total: {self.total_items}", key=self.total_items_key),
        ]

        pagination_controls = [
            sg.Button(
                "Previous",
                key=self.prev_key,
                disabled=(self.current_page <= 1),
                size=(8, 1),
            ),
            sg.Text(
                f"Page {self.current_page}/{self.total_pages}",
                key=self.page_info_key,
                size=(12, 1),
                justification="center",
            ),
            sg.Button(
                "Next",
                key=self.next_key,
                disabled=(self.current_page >= self.total_pages),
                size=(8, 1),
            ),
            sg.Push(),
        ]

        return [table_layout, pagination_layout, pagination_controls]

    def _load_data(self):
        try:
            result = self.data_callback(self.current_page, self.items_per_page)
            self.data = result.get("data", [])
            self.total_items = result.get("total", 0)
            self.total_pages = max(
                1, (self.total_items + self.items_per_page - 1) // self.items_per_page
            )
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            self.data = []
            self.total_items = 0
            self.total_pages = 1

    def handle_event(self, event: str, window: sg.Window) -> bool:
        if event == self.prev_key and self.current_page > 1:
            self.current_page -= 1
            self._load_data()
            self._update_ui(window)
            return True

        elif event == self.next_key and self.current_page < self.total_pages:
            self.current_page += 1
            self._load_data()
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
        self._load_data()
        self._update_ui(window)

    def get_selected_row_data(self, window: sg.Window) -> List[Any]:
        try:
            selected_rows = window[self.key].get()
            if selected_rows and len(selected_rows) > 0:
                selected_index = selected_rows[0]
                if 0 <= selected_index < len(self.data):
                    return self.data[selected_index]
        except Exception:
            pass
        return []
