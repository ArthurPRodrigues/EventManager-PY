import FreeSimpleGUI as sg

from events.application.list_event_use_case import ListEventInputDto
from friendship.ui.friendship_manager_gui import FriendshipManagerGUI
from shared.ui.base_gui import BaseGUI
from shared.ui.components import ActionButtonsComponent, HeaderComponent, TableComponent
from user.domain.user_role import UserRole


class ListEventGui(BaseGUI):
    def __init__(
        self, use_cases=None, navigator=None, auth_context=None, setup_event_map=True
    ):
        self.auth_context = auth_context
        title = self._get_title_by_role(auth_context)

        super().__init__(
            title=title,
            size=(900, 500),
            use_cases=use_cases,
            navigator=navigator,
            auth_context=auth_context,
        )

        self._setup_components_by_role()

        self.current_filter = "ALL"

        self.table = TableComponent(
            headers=[
                "id",
                "Name",
                "Created At",
                "Start Date",
                "End At",
                "Location",
                "Tickets Available",
            ],
            data_callback=self._load_events_callback,
            key="-TABLE-",
            items_per_page=10,
            has_hidden_id_column=True,
        )

        self.filter_group = [
            sg.Text("Filter:"),
            sg.Radio(
                "All", "FILTER", default=True, key="-FILTER_ALL-", enable_events=True
            ),
            sg.Radio(
                "With Tickets", "FILTER", key="-FILTER_TICKETS-", enable_events=True
            ),
            sg.Radio("Sold Out", "FILTER", key="-FILTER_SOLDOUT-", enable_events=True),
        ]

        self.event_map: dict[str, callable] = {}
        if setup_event_map:
            self._setup_event_map()

        self.extra_actions: list[sg.Button] = []
        if self.auth_context and self.auth_context.role == UserRole.ORGANIZER:
            self.extra_actions = [
                sg.Button("Edit Selected", key="-EDIT_SELECTED-"),
                sg.Button("Delete Selected", key="-DELETE_SELECTED-"),
            ]

    def window_refreshed(self):
        if not self.window:
            return
        try:
            self.table.refresh(self.window)
        except Exception as e:
            print(f"Error refreshing table: {e!s}")

    def _get_title_by_role(self, auth_context):
        if auth_context and auth_context.role == UserRole.ORGANIZER:
            return "Manage Events (Organizer)"
        if auth_context and auth_context.role == UserRole.CLIENT:
            return "List Events (Client)"
        return "Events"

    def _setup_components_by_role(self):
        self.header = HeaderComponent()
        self.header_extra_buttons: list[sg.Button] = []

        if self.auth_context and self.auth_context.role == UserRole.ORGANIZER:
            self.header_extra_buttons = [
                sg.Button("Create Event", key="-CREATE_EVENT-", size=(12, 1)),
                sg.Button("Tickets Redeemed", key="-TICKETS_REDEEMED-", size=(14, 1)),
                sg.Button("Validate Ticket", key="-VALIDATE_TICKET-", size=(14, 1)),
            ]
            self.action_buttons = ActionButtonsComponent([])
        elif self.auth_context and self.auth_context.role == UserRole.CLIENT:
            self.header_extra_buttons = [
                sg.Button("Manage Friends", key="-MANAGE_FRIENDS-", size=(14, 1)),
                sg.Button("My Tickets", key="-MY_TICKETS-", size=(12, 1)),
            ]
            self.action_buttons = ActionButtonsComponent([
                {"text": "Redeem Ticket", "key": "-REDEEM_TICKET-", "size": (14, 1)}
            ])
        else:
            self.action_buttons = ActionButtonsComponent([])

    def _setup_event_map(self):
        self.event_map.update({
            "-FILTER_ALL-": self._handle_filter_all,
            "-FILTER_TICKETS-": self._handle_filter_tickets,
            "-FILTER_SOLDOUT-": self._handle_filter_soldout,
        })

        if self.auth_context and self.auth_context.role == UserRole.ORGANIZER:
            self.event_map.update({
                "-CREATE_EVENT-": self._handle_create_event,
                "-VALIDATE_TICKET-": self._handle_validate_ticket,
                "-TICKETS_REDEEMED-": self._handle_ticket_redeemed,
                "-EDIT_SELECTED-": self._handle_edit_selected,
                "-DELETE_SELECTED-": self._handle_delete_selected,
            })

        if self.auth_context and self.auth_context.role == UserRole.CLIENT:
            self.event_map.update({
                "-MY_TICKETS-": self._handle_my_tickets,
                "-MANAGE_FRIENDS-": self._handle_manage_friends,
                "-REDEEM_TICKET-": self._handle_redeem_ticket,
            })

    def create_layout(self):
        layout = [*self.header.create_layout()]

        if getattr(self, "header_extra_buttons", None):
            row = [sg.Push()]
            for btn in self.header_extra_buttons:
                row.append(btn)
                row.append(sg.Push())
            layout.append(row)

        layout.extend([
            [sg.HorizontalSeparator()],
            [sg.Column([self.filter_group], pad=(0, 0))],
            [sg.Text("")],
            *self.table.create_layout(),
            [sg.Text("")],
            *self.action_buttons.create_layout(),
        ])
        if self.extra_actions:
            layout.extend([[sg.Text("")], [*self.extra_actions]])
        layout.append([sg.Text("")])
        return layout

    def handle_events(self, event, values):
        if self.table.handle_event(event, self.window):
            return
        handler = self.event_map.get(event)
        if handler:
            handler(values)

    def _handle_filter_all(self, _):
        self.current_filter = "ALL"
        self._refresh_table()

    def _handle_filter_tickets(self, _):
        self.current_filter = "TICKETS"
        self._refresh_table()

    def _handle_filter_soldout(self, _):
        self.current_filter = "SOLDOUT"
        self._refresh_table()

    def _refresh_table(self):
        if self.window:
            self.table.current_page = 1
            self.table.refresh(self.window)

    # Organizer
    def _handle_create_event(self, _):
        self.show_info_popup("Create Event not implemented yet")

    def _handle_validate_ticket(self, _):
        self.show_info_popup("Validate Ticket not implemented yet")

    def _handle_ticket_redeemed(self, _):
        self.show_info_popup("Tickets Redeemed not implemented yet")

    def _handle_edit_selected(self, _):
        data = self.table.get_selected_row_data(self.window)
        if not data:
            self.show_warning_popup("No row selected!")
            return
        self.show_info_popup(f"Edit not implemented (ID {data[0]})")

    def _handle_delete_selected(self, _):
        data = self.table.get_selected_row_data(self.window)
        if not data:
            self.show_warning_popup("No row selected!")
            return
        if self.show_confirmation_popup(
            f"Are you sure you want to delete event ID {data[0]}?"
        ):
            self.show_info_popup("Delete not implemented yet")

    # Client
    def _handle_my_tickets(self, _):
        self.show_info_popup("My Tickets not implemented yet")

    def _handle_manage_friends(self, _):
        if not self.navigator:
            self.show_warning_popup("Navigator not available.")
            return
        self.navigator.push_screen(FriendshipManagerGUI, auth_context=self.auth_context)

    def _handle_redeem_ticket(self, _):
        self.show_info_popup("Redeem Ticket not implemented yet")

    # evento calvback
    def _load_events_callback(self, page: int, items_per_page: int):
        try:
            organizer_id = None
            if self.auth_context and self.auth_context.role == UserRole.ORGANIZER:
                organizer_id = self.auth_context.id
            input_dto = ListEventInputDto(
                page=page,
                page_size=items_per_page,
                organizer_id=organizer_id,
            )
            result = self.use_cases.list_event_use_case.execute(input_dto)
            if result is None:
                return {"data": [], "total": 0}
            filtered = self._filter_events(result.items)
            table_data = self._convert_events_to_table_data(filtered)
            return {"data": table_data, "total": len(filtered)}
        except Exception:
            return {"data": [], "total": 0}

    def _filter_events(self, events):
        if self.current_filter == "ALL":
            return events
        if self.current_filter == "TICKETS":
            return [
                e
                for e in events
                if e.tickets_available is not None and e.tickets_available > 0
            ]
        if self.current_filter == "SOLDOUT":
            return [
                e
                for e in events
                if (e.tickets_available is not None and e.tickets_available == 0)
            ]
        return events

    def _convert_events_to_table_data(self, events):
        rows = []
        for event in events:
            created_at_str = "N/A"
            if hasattr(event, "created_at") and event.created_at:
                try:
                    created_at_str = event.created_at.strftime("%Y-%m-%d %H:%M")
                except Exception:
                    created_at_str = str(event.created_at)
            end_date_str = "N/A"
            if hasattr(event, "end_date") and event.end_date:
                try:
                    end_date_str = event.end_date.strftime("%Y-%m-%d %H:%M")
                except Exception:
                    end_date_str = str(event.end_date)
            start_date_str = "N/A"
            if hasattr(event, "start_date") and event.start_date:
                try:
                    start_date_str = event.start_date.strftime("%Y-%m-%d %H:%M")
                except Exception:
                    start_date_str = str(event.start_date)
            rows.append([
                event.id,
                event.name,
                created_at_str,
                start_date_str,
                end_date_str,
                event.location,
                event.tickets_available,
            ])
        return rows
