import FreeSimpleGUI as sg

from friendship.application.accept_friendship_invite_use_case import (
    AcceptFriendshipInviteInputDto,
)
from friendship.application.delete_friendship_use_case import DeleteFriendshipInputDto
from friendship.application.list_friendships_with_user_email_and_name_use_case import (
    ListFriendshipsInputDto,
)
from shared.ui.base_gui import BaseGUI
from shared.ui.components import ActionButtonsComponent, HeaderComponent, TableComponent


class FriendshipPendingInvitesGUI(BaseGUI):
    def __init__(self, use_cases=None):
        super().__init__(title="Friendship Manager", use_cases=use_cases)

        # TODO: Mock user ID, later integrate with auth system
        self.current_user_id = 1
        self.current_user_email = "joao@email.com"

        self.header = HeaderComponent(
            title="Pending Invites",
        )

        self.table = TableComponent(
            headers=["ID", "Name", "E-mail"],
            data_callback=self._load_friendships_callback,
            key="-TABLE-",
            items_per_page=10,
            has_hidden_id_column=True,
        )

        self.action_buttons = ActionButtonsComponent(
            [
                {
                    "text": "Accept Selected",
                    "key": "-ACCEPT_SELECTED-",
                    "size": (12, 1),
                },
                {
                    "text": "Decline Selected",
                    "key": "-DECLINE_SELECTED-",
                    "size": (12, 1),
                },
            ]
        )

        self.event_map = {
            "-ACCEPT_SELECTED-": self._handle_accept_selected,
            "-DECLINE_SELECTED-": self._handle_decline_selected,
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

    def _load_friendships_callback(self, page: int, items_per_page: int):
        try:
            input_dto = ListFriendshipsInputDto(
                page=page,
                size=items_per_page,
                requested_client_id=self.current_user_id,
                status="PENDING",
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
            friend_name = friendship.requested_name
            friend_email = friendship.requested_email

            friends_since = (
                friendship.accepted_at.strftime("%Y-%m-%d %H:%M:%S")
                if friendship.accepted_at
                else "N/A"
            )

            table_data.append([friendship.id, friend_name, friend_email, friends_since])

        return table_data

    def _handle_accept_selected(self, values):
        selected_data = self.table.get_selected_row_data(self.window)
        if selected_data:
            friendship_id = selected_data[0]
            friend_name = selected_data[1]

            if self.show_confirmation_popup(
                f"Are you sure you want to accept the friendship invite from: {friend_name}?"
            ):
                try:
                    input_dto = AcceptFriendshipInviteInputDto(
                        friendship_id=friendship_id,
                    )
                    self.use_cases.accept_friendship_invite_use_case.execute(input_dto)
                    self.show_info_popup(
                        f"Friendship invite from {friend_name} accepted successfully!"
                    )
                    self.table.refresh(self.window)
                except Exception as e:
                    self.show_error_popup(
                        f"Error accepting friendship invite: {str(e)}"
                    )
        else:
            self.show_warning_popup("No row selected!")

    def _handle_decline_selected(self, values):
        selected_data = self.table.get_selected_row_data(self.window)
        if selected_data:
            friendship_id = selected_data[0]
            friend_name = selected_data[1]

            if self.show_confirmation_popup(
                f"Are you sure you want to decline the friendship invite from: {friend_name}?"
            ):
                try:
                    input_dto = DeleteFriendshipInputDto(
                        friendship_id=friendship_id,
                    )
                    self.use_cases.delete_friendship_use_case.execute(input_dto)
                    self.show_info_popup(
                        f"Friendship invite from {friend_name} declined successfully!"
                    )
                    self.table.refresh(self.window)
                except Exception as e:
                    self.show_error_popup(
                        f"Error declining friendship invite: {str(e)}"
                    )
        else:
            self.show_warning_popup("No row selected!")

    def show(self):
        return super().show()


if __name__ == "__main__":
    app = FriendshipPendingInvitesGUI(use_cases=None)
    app.show()
