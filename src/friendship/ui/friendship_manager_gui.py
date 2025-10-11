from friendship.application.delete_friendship_use_case import DeleteFriendshipInputDto
from friendship.application.list_friendships_with_user_email_and_name_use_case import (
    ListFriendshipsInputDto,
)
from friendship.application.send_friendship_invite_use_case import (
    SendFriendshipInviteInputDto,
)
from friendship.domain.friendship_status import FriendshipStatus
from friendship.ui.friendship_pending_invites_gui import FriendshipPendingInvitesGUI
from shared.ui.base_gui import BaseGUI
from shared.ui.components import ActionButtonsComponent, HeaderComponent, TableComponent
from shared.ui.styles import BUTTON_SIZES, COLORS, WINDOW_SIZES


class FriendshipManagerGUI(BaseGUI):
    def __init__(self, use_cases=None, navigator=None, auth_context=None):
        super().__init__(
            title="Friendship Manager",
            size=WINDOW_SIZES["HORIZONTAL_DEFAULT"],
            use_cases=use_cases,
            navigator=navigator,
            auth_context=auth_context,
        )

        self.header = HeaderComponent(
            extra_buttons=[
                {
                    "text": "Pending Invites",
                    "key": "-PENDING-",
                    "size": BUTTON_SIZES["MEDIUM"],
                    "button_color": (COLORS["dark"], COLORS["secondary"]),
                }
            ]
        )

        self.table = TableComponent(
            headers=["ID", "NAME", "E-MAIL", "FRIENDS SINCE"],
            data_callback=self._load_friendships_callback,
            key="-TABLE-",
            items_per_page=10,
            has_hidden_id_column=True,
        )

        self.action_buttons = ActionButtonsComponent([
            {
                "text": "Add Friend",
                "key": "-ADD_FRIEND-",
                "button_color": (COLORS["white"], COLORS["success"]),
            },
            {
                "text": "Remove Selected",
                "key": "-REMOVE_SELECTED-",
                "size": BUTTON_SIZES["MEDIUM"],
                "button_color": (COLORS["white"], COLORS["warning"]),
            },
            {
                "text": "Transfer Ticket to Selected",
                "key": "-TRANSFER_TICKET-",
                "size": BUTTON_SIZES["EXTRA_LARGE"],
            },
        ])

        self.event_map = {
            "-PENDING-": self._handle_pending_invites,
            "-ADD_FRIEND-": self._handle_add_friend,
            "-REMOVE_SELECTED-": self._handle_remove_selected,
            "-TRANSFER_TICKET-": self._handle_transfer_ticket,
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

    def _handle_pending_invites(self, _):
        self.navigator.push_screen(
            FriendshipPendingInvitesGUI, auth_context=self.auth_context
        )

    def _handle_add_friend(self, _):
        confirmed, friend_email = self.show_input_dialog(
            dialog_title="Add friend",
            instruction_label="Enter Friend Email",
            input_tooltip="Enter the email address of the friend you want to add (e.g., friend@example.com)",
            confirm_button="Add Friend",
            cancel_button="Cancel",
        )

        if confirmed:
            if not friend_email:
                self.show_warning_popup("Please enter a valid email address!")
                return

            try:
                input_dto = SendFriendshipInviteInputDto(
                    requester_client_email=self.auth_context.email,
                    requested_client_email=friend_email,
                )
                self.use_cases.send_friendship_invite_use_case.execute(input_dto)
                self.show_info_popup(f"Friendship invite sent to: {friend_email}")
                self.table.refresh(self.window)
            except Exception as e:
                self.show_error_popup(f"Error sending friendship invite: {e!s}")

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
                participant_client_id=self.auth_context.id,
                status=FriendshipStatus.ACCEPTED,
            )

            paginated_friendships = self.use_cases.list_friendships_use_case.execute(
                input_dto
            )

            friendship_summaries, total_friendships_count = (
                paginated_friendships.friendship_summaries,
                paginated_friendships.total_friendships_count,
            )

            table_data = self._convert_friendships_to_table_data(friendship_summaries)

            return {"data": table_data, "total": total_friendships_count}

        except Exception as e:
            self.show_error_popup(f"Error loading friendships: {e}")
            return {"data": [], "total": 0}

    def _convert_friendships_to_table_data(self, friendships):
        table_data = []

        for friendship in friendships:
            if friendship.requester_client_id == self.auth_context.id:
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
