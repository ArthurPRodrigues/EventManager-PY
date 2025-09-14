import FreeSimpleGUI as sg

from shared.ui.base_gui import BaseGUI
from shared.ui.components import ActionButtonsComponent, HeaderComponent, TableComponent


class FriendshipManagerGUI(BaseGUI):
    def __init__(self):
        super().__init__(title="Friendship Manager")

        self.header = HeaderComponent(
            title="Friendship Manager",
            extra_button={
                "text": "Pending Invites",
                "key": "-PENDING-",
                "size": (12, 1),
            },
        )

        # TODO: Sample data for friends, remove when integrating with backend
        table_data = [
            ["Jorge", "jorge@email.com", "2024-01-15 14:30:00"],
            ["Ana", "ana@email.com", "2024-02-20 09:15:00"],
            ["Manoel", "manoel@email.com", "2024-03-10 16:45:00"],
        ]

        self.table = TableComponent(
            headers=["Name", "E-mail", "Friends Since"], data=table_data
        )

        self.action_buttons = ActionButtonsComponent(
            [
                {"text": "Add Friend", "key": "-ADD_FRIEND-", "size": (12, 1)},
                {
                    "text": "Remove Selected",
                    "key": "-REMOVE_SELECTED-",
                    "size": (15, 1),
                },
                {
                    "text": "Transfer Ticket to Selected",
                    "key": "-TRANSFER_TICKET-",
                    "size": (25, 1),
                },
            ]
        )

        self.event_map = {
            "-PENDING-": self._handle_pending_invites,
            "-ADD_FRIEND-": self._handle_add_friend,
            "-REMOVE_SELECTED-": self._handle_remove_selected,
            "-TRANSFER_TICKET-": self._handle_transfer_ticket,
        }

    def create_layout(self):
        layout = [
            *self.header.create_layout(),
            [sg.HorizontalSeparator()],
            [sg.Text("")],
            *self.table.create_layout(),
            [sg.Text("")],
            *self.action_buttons.create_layout(),
            [sg.Text("")],
        ]

        return layout

    def handle_events(self, event, values):
        handler = self.event_map.get(event)
        if handler:
            handler(values)
        elif event == "-TABLE-":
            pass

    def _handle_pending_invites(self, values):
        self.show_info_popup("Pending Invites button clicked!")

    def _handle_add_friend(self, values):
        self.show_info_popup("Add Friend button clicked!")

    def _handle_remove_selected(self, values):
        selected_rows = values["-TABLE-"]
        if selected_rows:
            self.show_info_popup(
                f"Remove Selected button clicked! Selected rows: {selected_rows}"
            )
        else:
            self.show_warning_popup("No row selected!")

    def _handle_transfer_ticket(self, values):
        selected_rows = values["-TABLE-"]
        if selected_rows:
            self.show_info_popup(
                f"Transfer Ticket button clicked! Selected rows: {selected_rows}"
            )
        else:
            self.show_warning_popup("No row selected!")

    def show(self):
        return super().show()


if __name__ == "__main__":
    app = FriendshipManagerGUI()
    app.show()
