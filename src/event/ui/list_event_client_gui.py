import FreeSimpleGUI as sg

from event.application.list_event_use_case import ListEventInputDto
from friendship.ui.friendship_manager_gui import FriendshipManagerGUI
from shared.ui.base_gui import BaseGUI
from shared.ui.components.action_buttons_component import ActionButtonsComponent
from shared.ui.components.header_component import HeaderComponent
from shared.ui.components.table_component import TableComponent
from shared.ui.styles import BUTTON_SIZES, COLORS, WINDOW_SIZES
from ticket.ui.redeem_ticket_gui import RedeemTicketGUI


class ListEventClientGui(BaseGUI):
    def __init__(self, use_cases=None, navigator=None, auth_context=None):
        super().__init__(
            title="Event List",
            size=WINDOW_SIZES["ARTHUR"],
            use_cases=use_cases,
            navigator=navigator,
            auth_context=auth_context,
        )

        self.header = HeaderComponent(
            extra_buttons=[
                {
                    "text": "My Tickets",
                    "key": "-MY_TICKETS-",
                    "size": BUTTON_SIZES["MEDIUM"],
                    "button_color": (COLORS["dark"], COLORS["secondary"]),
                },
                {
                    "text": "Manage Friends",
                    "key": "-MANAGE_FRIENDS-",
                    "size": BUTTON_SIZES["MEDIUM"],
                    "button_color": (COLORS["dark"], COLORS["secondary"]),
                },
            ]
        )
        self.current_filter_mode = "ALL"
        # TODO: update prototype
        # @ArthurPRodrigues
        self.table = TableComponent(
            headers=[
                "ID",
                "NAME",
                "LOCATION",
                "START DATE",
                "END DATE",
                "TICKETS AVAILABLE",
            ],
            data_callback=self._load_events_callback,
            key="-TABLE-",
            items_per_page=10,
            has_hidden_id_column=True,
        )

        self.action_buttons = ActionButtonsComponent([
            {
                "text": "Redeem Ticket",
                "key": "-REDEEM_TICKET-",
                "size": BUTTON_SIZES["EXTRA_LARGE"],
            },
        ])

        self.event_map = {
            "-MANAGE_FRIENDS-": self.handle_manage_friends,
            "-MY_TICKETS-": self.handle_tickets,
            "-REDEEM_TICKET-": self.handle_redeem_ticket,
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
        elif event == "-TABLE-":
            pass

    def handle_manage_friends(self):
        self.navigator.push_screen(FriendshipManagerGUI, auth_context=self.auth_context)

    def handle_tickets(self):
        # self.navigator.push_screen("TicketManagerGui", auth_context=self.auth_context)
        pass

    def handle_redeem_ticket(self):
        selected = self.table.get_selected_row_data(self.window)
        if not selected:
            self.show_warning_popup("Select an event first.")
            return

        event_id = selected[0]
        tickets_available = selected[5]

        self.navigator.push_screen(
            RedeemTicketGUI,
            auth_context=self.auth_context,
            event_id=event_id,
            tickets_available=tickets_available,
        )

    # TODO: Use the damn filter parameter on TableComponent instead of doing this manually
    # @ArthurPRodrigues
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
                event.location,
                event.start_date,
                event.end_date,
                event.tickets_available,
            ])
        return table_data
