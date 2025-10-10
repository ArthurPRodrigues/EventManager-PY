import os

import FreeSimpleGUI as sg

from shared.ui import BaseGUI
from shared.ui.components.action_buttons_component import ActionButtonsComponent
from shared.ui.components.header_component import HeaderComponent
from shared.ui.styles import COLORS, FONTS, LABEL_SIZES, WINDOW_SIZES
from user.application.create_user_use_case import CreateUserInputDto
from user.domain.user_role import UserRole


class CreateUserGUI(BaseGUI):
    def __init__(self, use_cases=None, navigator=None):
        super().__init__(
            title="Register User",
            size=WINDOW_SIZES["SQUARE_PANEL"],
            use_cases=use_cases,
            navigator=navigator,
        )

        self.roles = [role.value for role in UserRole]

        self.header = HeaderComponent()

        self.action_buttons = ActionButtonsComponent([
            {
                "text": "Create User",
                "key": "-CREATE-",
                "font": FONTS["PRIMARY_BUTTON"],
                "button_color": (COLORS["dark"], COLORS["secondary"]),
            },
        ])

        self.event_map = {
            "-CREATE-": self._handle_create_user,
        }

    def create_layout(self):
        labels = [
            [
                sg.Text(
                    "Name*",
                    font=FONTS["LABEL"],
                    size=LABEL_SIZES["DEFAULT"],
                    pad=(0, 10),
                ),
            ],
            [
                sg.Text(
                    "Email*",
                    font=FONTS["LABEL"],
                    size=LABEL_SIZES["DEFAULT"],
                    pad=(0, 10),
                ),
            ],
            [
                sg.Text(
                    "Password*",
                    font=FONTS["LABEL"],
                    size=LABEL_SIZES["DEFAULT"],
                    pad=(0, 10),
                ),
            ],
            [
                sg.Text(
                    "Role*",
                    font=FONTS["LABEL"],
                    size=LABEL_SIZES["DEFAULT"],
                    pad=(0, 10),
                ),
            ],
        ]

        inputs = [
            [
                sg.Input(
                    key="-NAME-",
                    tooltip="Enter your full name",
                    font=FONTS["INPUT"],
                    pad=(0, 10),
                ),
            ],
            [
                sg.Input(
                    key="-EMAIL-",
                    tooltip="Enter your email (e.g., user@email.com)",
                    font=FONTS["INPUT"],
                    pad=(0, 10),
                ),
            ],
            [
                sg.Input(
                    key="-PASSWORD-",
                    password_char="*",
                    tooltip="Enter your password",
                    font=FONTS["INPUT"],
                    pad=(0, 10),
                ),
            ],
            [
                sg.Combo(
                    self.roles,
                    default_value=self.roles[0],
                    key="-ROLE-",
                    readonly=True,
                    tooltip="Select your role in the system",
                    font=FONTS["INPUT"],
                    pad=(0, 10),
                ),
            ],
        ]

        layout = [
            *self.header.create_layout(),
            [
                sg.Text(
                    "CREATE YOUR ACCOUNT",
                    font=FONTS["TITLE_MAIN"],
                    justification="center",
                    pad=((0, 5), (20, 0)),
                ),
                sg.Image(
                    filename=os.path.join("assets", "png", "tada_32x32.png"),
                ),
            ],
            [
                sg.Text(
                    "Create an account to manage\nand discover new events.",
                    font=FONTS["SUBTITLE"],
                    justification="center",
                    pad=(20, 20),
                    text_color=COLORS["secondary"],
                ),
            ],
            [
                sg.Column(
                    labels,
                    element_justification="left",
                    vertical_alignment="top",
                    pad=((30, 0), (0, 0)),
                ),
                sg.Column(
                    inputs,
                    element_justification="left",
                    vertical_alignment="top",
                    pad=((0, 30), (0, 0)),
                ),
            ],
            [
                sg.Checkbox(
                    "I confirm I am 18 years or older*",
                    key="-AGE_CONFIRM-",
                    font=FONTS["CHECKBOX"],
                    enable_events=False,
                    expand_x=True,
                    pad=(20, 10),
                    checkbox_color=(COLORS["primary_lighter"]),
                )
            ],
            [
                sg.Text(
                    "Fields marked with * are required",
                    text_color=COLORS["info"],
                    font=FONTS["FOOTNOTE"],
                    expand_x=True,
                    justification="left",
                    pad=((30, 0), (0, 0)),
                ),
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
