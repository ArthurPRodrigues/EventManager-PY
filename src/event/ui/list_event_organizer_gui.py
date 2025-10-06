from event.application.list_event_use_case import ListEventInputDto
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
        self.table = TableComponent(
            headers=[
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
        if self.table.handle_event(event, self.window):
            return

        handler = self.event_map.get(event)
        if handler:
            handler()
        elif event == "-TABLE-":
            pass

    def handle_validate_ticket(self):
        self.navigator.navigate_to("validate_ticket")

    def handle_tickets_redeemed(self):
        self.navigator.navigate_to("tickets_redeemed")

    def handle_create_event(self):
        self.navigator.navigate_to("create_event")

    def handle_delete_selected(self):
        self.navigator.navigate_to("delete_selected")

    def handle_edit_selected(self):
        self.navigator.navigate_to("edit_selected")

    def create_layout(self):
        layout = [
            *self.header.create_layout(),
            *self.table.create_layout(),
            *self.action_buttons.create_layout(),
        ]
        return layout

    def _load_events_callback(self, page: int, items_per_page: int):
        try:
            input_dto = ListEventInputDto(
                page=page,
                page_size=items_per_page,
            )

            paginated_events = self.use_cases.list_event_use_case.execute(input_dto)

            event_list, total_event_count = (
                paginated_events.event_list,
                paginated_events.total_event_count,
            )

            table_data = self._convert_events_to_table_data(event_list)
            return {"data": table_data, "total_event_count": total_event_count}
        except Exception as e:
            self.show_error_popup(f"Error loading events: {e}")
            return {"data": [], "total_event_count": 0}

    def _convert_events_to_table_data(self, events):
        table_data = []

        for event in events:
            table_data.append([
                event.name,
                event.location,
                event.created_at,
                event.start_date,
                event.end_date,
                event.tickets_available,
            ])
        return table_data
