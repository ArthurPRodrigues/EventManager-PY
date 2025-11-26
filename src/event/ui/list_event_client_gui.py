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
                    "text": "Manage Friends",
                    "key": "-MANAGE_FRIENDS-",
                    "size": BUTTON_SIZES["MEDIUM"],
                    "button_color": (COLORS["dark"], COLORS["secondary"]),
                },
                {
                    "text": "My Tickets",
                    "key": "-MY_TICKETS-",
                    "size": BUTTON_SIZES["MEDIUM"],
                    "button_color": (COLORS["dark"], COLORS["secondary"]),
                },
            ]
        )
        event_filters = [
            {
                "text": "All",
                "group_id": "EVENT_FILTER",
                "default": True,
                "filter_value": "ALL",
            },
            {
                "text": "With Tickets",
                "group_id": "EVENT_FILTER",
                "filter_value": "WITH_TICKETS",
            },
            {
                "text": "Sold Out",
                "group_id": "EVENT_FILTER",
                "filter_value": "SOLD_OUT",
            },
        ]
        self.table = TableComponent(
            headers=[
                "ID",
                "NAME",
                "LOCATION",
                "START DATE",
                "END DATE",
                "STATUS",
                "TICKETS",
            ],
            data_callback=self._load_events_callback,
            key="-TABLE-",
            items_per_page=8,
            has_hidden_id_column=True,
            filters=event_filters,
        )

        self.action_buttons = ActionButtonsComponent([
            {
                "text": "Redeem Ticket",
                "key": "-REDEEM_TICKET-",
                "size": BUTTON_SIZES["EXTRA_LARGE"],
                "disabled": True,
            },
        ])

        self.event_map = {
            "-MANAGE_FRIENDS-": self.handle_manage_friends,
            "-MY_TICKETS-": self.handle_tickets,
            "-REDEEM_TICKET-": self.handle_redeem_ticket,
        }

    def _status_indicator(
        self, initial_max_tickets, max_tickets, tickets_redeemed
    ) -> str:
        tickets_available = max_tickets - tickets_redeemed
        if tickets_available > round(initial_max_tickets / 2):
            return "🔵 Blue"
        else:
            return "🔴 Red"

    def _tickets_available(self, max_tickets, tickets_redeemed):
        tickets_available = max(0, max_tickets - tickets_redeemed)
        return tickets_available

    def handle_events(self, event, values):
        if self.table.handle_event(event, self.window):
            self._update_redeem_button_state()
            return

        handler = self.event_map.get(event)
        if handler:
            handler()
        elif event == "-TABLE-":
            self._update_redeem_button_state()

    def handle_manage_friends(self):
        self.navigator.push_screen(FriendshipManagerGUI, auth_context=self.auth_context)

    def handle_tickets(self):
        self.show_warning_popup("Not implemented.")

    def handle_redeem_ticket(self):
        selected = self.table.get_selected_row_data(self.window)

        event_id = selected[0]
        max_tickets = selected[7]
        tickets_redeemed = selected[8]

        self.navigator.push_screen(
            RedeemTicketGUI,
            auth_context=self.auth_context,
            event_id=event_id,
            max_tickets=max_tickets,
            tickets_redeemed=tickets_redeemed,
        )

    def create_layout(self):
        layout = [
            *self.header.create_layout(),
            *self.table.create_layout(),
            *self.action_buttons.create_layout(),
        ]
        return layout

    def _load_events_callback(self, page: int, items_per_page: int, filter_mode: str):
        try:
            input_dto = ListEventInputDto(
                page=page,
                page_size=items_per_page,
                filter_mode=filter_mode,
                user_id=self.auth_context.id,
            )
            paginated_events = self.use_cases.list_event_use_case.list_event(input_dto)

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
                event.start_date.astimezone().strftime("%d/%m/%Y %Hh%M"),
                event.end_date.astimezone().strftime("%d/%m/%Y %Hh%M"),
                self._status_indicator(
                    event.initial_max_tickets, event.max_tickets, event.tickets_redeemed
                ),
                self._tickets_available(event.max_tickets, event.tickets_redeemed),
                event.max_tickets,
                event.tickets_redeemed,
            ])
        return table_data

    def _update_redeem_button_state(self):
        try:
            selected = self.table.get_selected_row_data(self.window)
            is_enabled = bool(selected)
            if self.window:
                self.window["-REDEEM_TICKET-"].update(disabled=not is_enabled)
        except Exception:
            if self.window:
                self.window["-REDEEM_TICKET-"].update(disabled=True)
