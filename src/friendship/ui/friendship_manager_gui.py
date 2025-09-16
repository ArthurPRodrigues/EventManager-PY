import FreeSimpleGUI as sg

from friendship.application.delete_friendship_use_case import DeleteFriendshipInputDto
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
            headers=["ID", "Name", "E-mail", "Friends Since"],
            data_callback=self._load_friendships_callback,
            key="-TABLE-",
            items_per_page=10,
            has_hidden_id_column=True,
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
        if self.table.handle_event(event, self.window):
            return

        handler = self.event_map.get(event)
        if handler:
            handler(values)
        elif event == "-TABLE-":
            pass

    def _handle_pending_invites(self, values):
        self.show_info_popup("Pending Invites button clicked!")

    def _handle_add_friend(self, values):
        self.show_info_popup("Add Friend button clicked!")

    def _handle_remove_selected(self, _):
        selected_data = self.table.get_selected_row_data(self.window)
        if selected_data:
            friendship_id = selected_data[0]
            friend_name = selected_data[1]
            if self.show_confirmation_popup(
                f"Are you sure you want to remove: {friend_name} from your friends?"
            ):
                try:
                    input_dto = DeleteFriendshipInputDto(
                        friendship_id=friendship_id,
                    )
                    self.use_cases.delete_friendship_use_case.execute(input_dto)
                    self.show_info_popup(f"Friend {friend_name} removed successfully!")
                    self.table.refresh(self.window)
                except Exception as e:
                    self.show_error_popup(f"Error removing friend: {e}")
        else:
            self.show_warning_popup("No row selected!")

    def _handle_transfer_ticket(self, values):
        selected_data = self.table.get_selected_row_data(self.window)
        if selected_data:
            self.show_info_popup(
                f"Transfer Ticket button clicked! Selected friend: {selected_data[1]} ({selected_data[2]})"
            )
        else:
            self.show_warning_popup("No row selected!")

    def _load_friendships_callback(self, page: int, items_per_page: int):
        try:
            input_dto = ListFriendshipsInputDto(
                page=page,
                size=items_per_page,
                participant_client_id=self.current_user_id,
                status="ACCEPTED",
            )

            friendships, total = self.use_cases.list_friendships_use_case.execute(
                input_dto
            )

            table_data = self._convert_friendships_to_table_data(friendships)

            return {"data": table_data, "total": total}

        except Exception as e:
            print(f"Erro ao carregar amizades: {str(e)}")
            return {"data": [], "total": 0}

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

            table_data.append([friendship.id, friend_name, friend_email, friends_since])

        return table_data

    def show(self):
        return super().show()


if __name__ == "__main__":
    app = FriendshipManagerGUI(use_cases=None)
    app.show()
