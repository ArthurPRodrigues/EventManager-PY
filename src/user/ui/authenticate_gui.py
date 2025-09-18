import FreeSimpleGUI as sg

from shared.ui.base_gui import BaseGUI
from shared.ui.components import ActionButtonsComponent

#from user.application.authenticate_user_use_case import AuthenticateUserInputDto
from user.domain.user_role import UserRole


class AuthenticateGUI(BaseGUI):
    def __init__(self, use_cases=None, navigator=None):
        super().__init__(
            title="Login", use_cases=use_cases, navigator=navigator
        )

        self.roles = [role.value for role in UserRole]

        self.action_buttons = ActionButtonsComponent(
            [
                {"text": "Login", "key": "-LOGIN-", "size": (12, 1)},
                {
                    "text": "Create User",
                    "key": "-CREATE_USER-",
                    "size": (12, 1),
                },
            ]
        )

        self.event_map = {
            "-LOGIN-": self._handle_user_login,
            "-CREATE_USER-": self._handle_create_user
        }

    def create_layout(self):
        layout = [
            [sg.Text("Email", size=(8,1)), sg.Input(key="-EMAIL-")],
            [sg.Text("Password", size=(8,1)), sg.Input(key="-PASSWORD-", password_char="*")],
            [sg.Text("Role", size=(8,1)),
             sg.Combo(self.roles, default_value=self.roles[0], key="-ROLE-", readonly=True)],
            *self.action_buttons.create_layout(),
        ]

        return layout

    def handle_events(self, event, values):
        handler = self.event_map.get(event)
        if handler:
            handler(values)

    def _handle_user_login(self, values):

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

    def _handle_create_user(self):
        pass

    # def _handle_pending_invites(self, _):
    #     self.navigator.push_screen(FriendshipPendingInvitesGUI)

    # def _handle_add_friend(self, _):
    #     confirmed, friend_email = self.show_input_dialog(
    #         dialog_title="Add friend",
    #         instruction_label="Enter Friend Email",
    #         input_placeholder="",
    #         confirm_button="Add Friend",
    #         cancel_button="Cancel",
    #     )

    #     if confirmed:
    #         if not friend_email:
    #             self.show_warning_popup("Please enter a valid email address!")
    #             return

    #         try:
    #             input_dto = SendFriendshipInviteInputDto(
    #                 requester_client_email=self.current_user_email,
    #                 requested_client_email=friend_email,
    #             )
    #             self.use_cases.send_friendship_invite_use_case.execute(input_dto)
    #             self.show_info_popup(f"Friendship invite sent to: {friend_email}")
    #             self.table.refresh(self.window)
    #         except Exception as e:
    #             self.show_error_popup(f"Error sending friendship invite: {str(e)}")

    # def _handle_remove_selected(self, _):
    #     selected_data = self.table.get_selected_row_data(self.window)
    #     if selected_data:
    #         friendship_id = selected_data[0]
    #         friend_name = selected_data[1]
    #         if self.show_confirmation_popup(
    #             f"Are you sure you want to remove: {friend_name} from your friends?"
    #         ):
    #             try:
    #                 input_dto = DeleteFriendshipInputDto(
    #                     friendship_id=friendship_id,
    #                 )
    #                 self.use_cases.delete_friendship_use_case.execute(input_dto)
    #                 self.show_info_popup(f"Friend {friend_name} removed successfully!")
    #                 self.table.refresh(self.window)
    #             except Exception as e:
    #                 self.show_error_popup(f"Error removing friend: {e}")
    #     else:
    #         self.show_warning_popup("No row selected!")

    # def _handle_transfer_ticket(self, values):
    #     selected_data = self.table.get_selected_row_data(self.window)
    #     if selected_data:
    #         self.show_info_popup(
    #             f"Transfer Ticket button clicked! Selected friend: {selected_data[1]} ({selected_data[2]})"
    #         )
    #     else:
    #         self.show_warning_popup("No row selected!")

    # def _load_friendships_callback(self, page: int, items_per_page: int):
    #     try:
    #         input_dto = ListFriendshipsInputDto(
    #             page=page,
    #             size=items_per_page,
    #             participant_client_id=self.current_user_id,
    #             status="ACCEPTED",
    #         )

    #         friendships, total = self.use_cases.list_friendships_use_case.execute(
    #             input_dto
    #         )

    #         table_data = self._convert_friendships_to_table_data(friendships)

    #         return {"data": table_data, "total": total}

    #     except Exception as e:
    #         print(f"Erro ao carregar amizades: {str(e)}")
    #         return {"data": [], "total": 0}

    # def _convert_friendships_to_table_data(self, friendships):
    #     table_data = []

    #     for friendship in friendships:
    #         if friendship.requester_client_id == self.current_user_id:
    #             friend_name = friendship.requested_name
    #             friend_email = friendship.requested_email
    #         else:
    #             friend_name = friendship.requester_name
    #             friend_email = friendship.requester_email

    #         friends_since = (
    #             friendship.accepted_at.strftime("%Y-%m-%d %H:%M:%S")
    #             if friendship.accepted_at
    #             else "N/A"
    #         )

    #         table_data.append([friendship.id, friend_name, friend_email, friends_since])

    #     return table_data

    def show(self):
        return super().show()
