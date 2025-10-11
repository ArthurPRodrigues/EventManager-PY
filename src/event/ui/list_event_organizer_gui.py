import FreeSimpleGUI as sg

from event.application.list_event_use_case import ListEventInputDto
from event.ui.create_event_gui import CreateEventGUI
from shared.ui.base_gui import BaseGUI
from shared.ui.components.action_buttons_component import ActionButtonsComponent
from shared.ui.components.header_component import HeaderComponent
from shared.ui.components.table_component import TableComponent
from shared.ui.styles import BUTTON_SIZES, COLORS, WINDOW_SIZES


class ListEventOrganizerGui(BaseGUI):
    def __init__(self, use_cases=None, navigator=None, auth_context=None):
        super().__init__(
            title="Event Organizer",
            size=WINDOW_SIZES["ARTHUR"],
            use_cases=use_cases,
            navigator=navigator,
            auth_context=auth_context,
        )

        self.header = HeaderComponent(
            extra_buttons=[
                {
                    "text": "Validate Ticket",
                    "key": "-VALIDATE_TICKET-",
                    "size": BUTTON_SIZES["MEDIUM"],
                    "button_color": (COLORS["dark"], COLORS["secondary"]),
                },
                {
                    "text": "Tickets Redeemed",
                    "key": "-TICKETS_REDEEMED-",
                    "size": BUTTON_SIZES["MEDIUM"],
                    "button_color": (COLORS["dark"], COLORS["secondary"]),
                },
                {
                    "text": "Create Event",
                    "key": "-CREATE_EVENT-",
                    "size": BUTTON_SIZES["MEDIUM"],
                    "button_color": (COLORS["dark"], COLORS["secondary"]),
                },
            ]
        )
        self.current_filter_mode = "ALL"
        self.table = TableComponent(
            headers=[
                "ID",
                "NAME",
                "CREATED AT",
                "START DATE",
                "END DATE",
                "LOCATION",
                "TICKETS",
            ],
            data_callback=self._load_events_callback,
            key="-TABLE-",
            items_per_page=10,
            has_hidden_id_column=True,
        )
        self.action_buttons = ActionButtonsComponent([
            {
                "text": "Delete Selected",
                "key": "-DELETE_SELECTED-",
                "size": BUTTON_SIZES["EXTRA_LARGE"],
            },
            {
                "text": "Edit Selected",
                "key": "-EDIT_SELECTED-",
                "size": BUTTON_SIZES["EXTRA_LARGE"],
            },
        ])

        self.event_map = {
            "-VALIDATE_TICKET-": self.handle_validate_ticket,
            "-TICKETS_REDEEMED-": self.handle_tickets_redeemed,
            "-CREATE_EVENT-": self.handle_create_event,
            "-DELETE_SELECTED-": self.handle_delete_selected,
            "-EDIT_SELECTED-": self.handle_edit_selected,
        }

    def handle_events(self, event, values):
        if event in ("-ORG_F_ALL-", "-ORG_F_WITH-", "-ORG_F_SOLD-"):
            if values.get("-ORG_F_ALL-"):
                self.current_filter_mode = "ALL"
            elif values.get("-ORG_F_WITH-"):
                self.current_filter_mode = "WITH_TICKETS"
            elif values.get("-ORG_F_SOLD-"):
                self.current_filter_mode = "SOLD_OUT"
            if self.window:
                self.table.current_page = 1
                self.table.refresh(self.window)
            return

        if self.table.handle_event(event, self.window):
            return

        handler = self.event_map.get(event)
        if handler:
            handler()

    def handle_validate_ticket(self):
        self.navigator.navigate_to("validate_ticket")

    def handle_tickets_redeemed(self):
        self.navigator.navigate_to("tickets_redeemed")

    def handle_create_event(self):
        self.navigator.push_screen(CreateEventGUI, auth_context=self.auth_context)

    def handle_delete_selected(self):
        self.navigator.navigate_to("delete_selected")

    def handle_edit_selected(self):
        self.navigator.navigate_to("edit_selected")

    def create_layout(self):
        filter_row = [
            sg.Text("Filter:"),
            sg.Radio(
                "All", "ORG_FILTER", key="-ORG_F_ALL-", default=True, enable_events=True
            ),
            sg.Radio(
                "With Tickets", "ORG_FILTER", key="-ORG_F_WITH-", enable_events=True
            ),
            sg.Radio("Sold Out", "ORG_FILTER", key="-ORG_F_SOLD-", enable_events=True),
        ]
        layout = [
            *self.header.create_layout(),
            filter_row,
            *self.table.create_layout(),
            *self.action_buttons.create_layout(),
        ]
        return layout

    def _load_events_callback(self, page: int, items_per_page: int):
        try:
            input_dto = ListEventInputDto(
                page=page,
                page_size=items_per_page,
                organizer_id=self.auth_context.id,
                filter_mode=self.current_filter_mode,
            )

            paginated_events = self.use_cases.list_event_use_case.execute(input_dto)

            event_list, total_event_count = (
                paginated_events.event_list,
                paginated_events.total_event_count,
            )

            table_data = self._convert_events_to_table_data(event_list)
            return {"data": table_data, "total": total_event_count}
        except Exception as e:
            self.show_error_popup(f"Error loading events: {e}")
            return {"data": [], "total": 0}

    def _convert_events_to_table_data(self, events):
        table_data = []

        for event in events:
            table_data.append([
                event.id,
                event.name,
                event.created_at,
                event.start_date,
                event.end_date,
                event.location,
                event.tickets_available,
            ])
        return table_data
