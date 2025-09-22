import FreeSimpleGUI as sg

from friendship.ui.friendship_manager_gui import FriendshipManagerGUI
from shared.domain.auth_context import AuthContext
from shared.ui.base_gui import BaseGUI
from shared.ui.components import ActionButtonsComponent
from user.application.authenticate_user_use_case import AuthenticateUserInputDto
from user.domain.user import User
from user.domain.user_role import UserRole
from user.ui.create_user_gui import CreateUserGUI


class AuthenticateGUI(BaseGUI):
    def __init__(self, use_cases=None, navigator=None):
        super().__init__(
            title="Login", size=(400, 140), use_cases=use_cases, navigator=navigator
        )

        self.roles = [role.value for role in UserRole]

        self.action_buttons = ActionButtonsComponent([
            {"text": "Login", "key": "-LOGIN-", "size": (12, 1)},
            {"text": "Create User", "key": "-CREATE_USER-", "size": (12, 1)},
        ])

        self.event_map = {
            "-LOGIN-": self._handle_user_login,
            "-CREATE_USER-": self._handle_create_user,
        }

    def create_layout(self):
        layout = [
            [sg.Text("Email", size=(8, 1)), sg.Input(key="-EMAIL-")],
            [
                sg.Text("Password", size=(8, 1)),
                sg.Input(key="-PASSWORD-", password_char="*"),
            ],
            [
                sg.Text("Role", size=(8, 1)),
                sg.Combo(
                    self.roles,
                    default_value=self.roles[0],
                    key="-ROLE-",
                    readonly=True,
                ),
            ],
            *self.action_buttons.create_layout(),
        ]

        return layout

    def handle_events(self, event, values):
        handler = self.event_map.get(event)
        if handler:
            handler(values)

    def _handle_user_login(self, values):
        email = values.get("-EMAIL-")
        password = values.get("-PASSWORD-")
        role = values.get("-ROLE-")

        if not email or not password or not role:
            self.show_warning_popup("Please fill all fields.")
            return

        try:
            input_dto = AuthenticateUserInputDto(
                email=email, password=password, role=UserRole(role)
            )
            user = self.use_cases.authenticate_user_use_case.execute(input_dto)
            self._set_auth_context(user)
            self.show_info_popup(
                f"Welcome, {self.auth_context.name} ({self.auth_context.role.value})!"
            )

            if self.auth_context.role.value == "CLIENT":
                self.navigator.push_screen(
                    FriendshipManagerGUI, auth_context=self.auth_context
                )
            else:
                self.show_info_popup(
                    "Interfaces for ORGANIZER and STAFF are not implemented yet."
                )

        except Exception as e:
            self.show_error_popup(f"Error authenticating user: {e}")

    def _handle_create_user(self, values):
        self.navigator.push_screen(CreateUserGUI)

    def _set_auth_context(self, user: User):
        self.auth_context = AuthContext(
            id=user.id, name=user.name, email=user.email, role=user.role
        )

    def show(self):
        return super().show()
