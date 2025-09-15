import FreeSimpleGUI as sg

from friendship.application.list_friendships_with_user_email_and_name_use_case import (
    ListFriendshipsInputDto,
)
from shared.ui.base_gui import BaseGUI
from shared.ui.components import ActionButtonsComponent, HeaderComponent, TableComponent


class FriendshipManagerGUI(BaseGUI):
    def __init__(self, use_cases=None):
        super().__init__(title="Friendship Manager", use_cases=use_cases)

        # TODO: Mock user ID, later integrate with auth system
        self.current_user_id = 1

        self.header = HeaderComponent(
            title="Friendship Manager",
            extra_button={
                "text": "Pending Invites",
                "key": "-PENDING-",
                "size": (12, 1),
            },
        )

        self.table = TableComponent(
            headers=["Name", "E-mail", "Friends Since"], data=[]
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
        self._load_friendships()
        return super().show()

    def _load_friendships(self):
        try:
            input_dto = ListFriendshipsInputDto(
                page=1,
                size=50,
                participant_client_id=self.current_user_id,
                status="ACCEPTED",
            )

            friendships, total = self.use_cases.list_friendships_use_case.execute(
                input_dto
            )

            table_data = self._convert_friendships_to_table_data(friendships)
            self.table.update_data(table_data)

        except Exception as e:
            self.show_warning_popup(f"Erro ao carregar amizades: {str(e)}")

    def _convert_friendships_to_table_data(self, friendships):
        table_data = []

        for friendship in friendships:
            if friendship.requester_client_id == self.current_user_id:
                friend_name = friendship.requested_name
                friend_email = friendship.requested_email
            else:
                friend_name = friendship.requester_name
                friend_email = friendship.requester_email

            friends_since = (
                friendship.accepted_at.strftime("%Y-%m-%d %H:%M:%S")
                if friendship.accepted_at
                else "N/A"
            )

            table_data.append([friend_name, friend_email, friends_since])

        return table_data


if __name__ == "__main__":
    app = FriendshipManagerGUI(use_cases=None)
    app.show()
