from friendship.application.accept_friendship_invite_use_case import (
    AcceptFriendshipInviteInputDto,
)
from friendship.application.delete_friendship_use_case import DeleteFriendshipInputDto
from friendship.application.list_friendships_with_user_email_and_name_use_case import (
    ListFriendshipsInputDto,
)
from friendship.domain.friendship_status import FriendshipStatus
from shared.ui.base_gui import BaseGUI
from shared.ui.components import ActionButtonsComponent, HeaderComponent, TableComponent
from shared.ui.styles import BUTTON_SIZES, COLORS, WINDOW_SIZES


class FriendshipPendingInvitesGUI(BaseGUI):
    def __init__(self, use_cases=None, navigator=None, auth_context=None):
        super().__init__(
            title="Pending Invites",
            size=WINDOW_SIZES["HORIZONTAL_DEFAULT"],
            use_cases=use_cases,
            navigator=navigator,
            auth_context=auth_context,
        )

        self.header = HeaderComponent()

        self.table = TableComponent(
            headers=["ID", "NAME", "E-MAIL"],
            data_callback=self._load_friendships_callback,
            key="-TABLE-",
            items_per_page=10,
            has_hidden_id_column=True,
        )

        self.action_buttons = ActionButtonsComponent([
            {
                "text": "Accept Selected",
                "key": "-ACCEPT_SELECTED-",
                "button_color": (COLORS["white"], COLORS["success"]),
                "size": BUTTON_SIZES["MEDIUM"],
            },
            {
                "text": "Decline Selected",
                "key": "-DECLINE_SELECTED-",
                "button_color": (COLORS["white"], COLORS["warning"]),
                "size": BUTTON_SIZES["MEDIUM"],
            },
        ])

        self.event_map = {
            "-ACCEPT_SELECTED-": self._handle_accept_selected,
            "-DECLINE_SELECTED-": self._handle_decline_selected,
        }

    def create_layout(self):
        layout = [
            *self.header.create_layout(),
            *self.table.create_layout(),
            *self.action_buttons.create_layout(),
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
                requested_client_id=self.auth_context.id,
                status=FriendshipStatus.PENDING,
            )

            friendships, total = self.use_cases.list_friendships_use_case.execute(
                input_dto
            )

            table_data = self._convert_friendships_to_table_data(friendships)

            return {"data": table_data, "total": total}
        # TODO: show popup error instead of print
        except Exception as e:
            print(f"Erro ao carregar amizades: {e!s}")
            return {"data": [], "total": 0}

    def _convert_friendships_to_table_data(self, friendships):
        table_data = []

        for friendship in friendships:
            friend_name = friendship.requester_name
            friend_email = friendship.requester_email

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
                    self.show_error_popup(f"Error accepting friendship invite: {e!s}")
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
                    self.show_error_popup(f"Error declining friendship invite: {e!s}")
        else:
            self.show_warning_popup("No row selected!")
