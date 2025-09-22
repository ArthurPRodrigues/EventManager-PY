import FreeSimpleGUI as sg

from shared.ui import BaseGUI
from shared.ui.components.action_buttons_component import ActionButtonsComponent
from user.application.create_user_use_case import CreateUserInputDto
from user.domain.user_role import UserRole


class CreateUserGUI(BaseGUI):
    def __init__(self, use_cases=None, navigator=None):
        super().__init__(
            title="Register User",
            size=(400, 300),
            use_cases=use_cases,
            navigator=navigator,
        )

        self.roles = [role.value for role in UserRole]

        self.action_buttons = ActionButtonsComponent([
            {"text": "Create User", "key": "-CREATE-", "size": (12, 1)},
        ])

        self.event_map = {
            "-CREATE-": self._handle_create_user,
        }

    def create_layout(self):
        layout = [
            [sg.Button("Back", key="-BACK-"), sg.Push()],
            [
                sg.Text(
                    "Register",
                    font=("Helvetica", 20),
                    justification="center",
                    expand_x=True,
                )
            ],
            [sg.HorizontalSeparator()],
            [sg.Text("Name*", size=(8, 1)), sg.Input(key="-NAME-")],
            [sg.Text("Email*", size=(8, 1)), sg.Input(key="-EMAIL-")],
            [
                sg.Text("Password*", size=(8, 1)),
                sg.Input(key="-PASSWORD-", password_char="*"),
            ],
            [
                sg.Text("Role*", size=(8, 1)),
                sg.Combo(
                    self.roles, default_value=self.roles[0], key="-ROLE-", readonly=True
                ),
            ],
            [
                sg.Checkbox(
                    "I confirm I am 18 years or older*",
                    key="-AGE_CONFIRM-",
                    enable_events=False,
                )
            ],
            *self.action_buttons.create_layout(),
        ]

        return layout

    def handle_events(self, event, values):
        handler = self.event_map.get(event)
        if handler:
            handler(values)

    def _handle_create_user(self, values):
        name = values.get("-NAME-")
        email = values.get("-EMAIL-")
        password = values.get("-PASSWORD-")
        role_str = values.get("-ROLE-")
        age_confirmed = values.get("-AGE_CONFIRM-")

        if not name or not email or not password or not role_str:
            self.show_warning_popup("Please fill all fields.")
            return

        if not age_confirmed:
            self.show_warning_popup(
                "Please confirm that you are 18 years old or older."
            )
            return

        try:
            input_dto = CreateUserInputDto(
                name=name, email=email, password=password, role=UserRole(role_str)
            )

            user = self.use_cases.create_user_use_case.execute(input_dto)

            self.show_info_popup(
                f"User '{user.name}' for {user.role.value} role created successfully!"
            )

            self.navigator.pop_screen()

        except Exception as e:
            self.show_error_popup(f"Error creating user: {e!s}")
