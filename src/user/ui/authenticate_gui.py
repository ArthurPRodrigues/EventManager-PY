import os

import FreeSimpleGUI as sg

from events.ui.list_events_gui import ListEventsGui
from shared.domain.auth_context import AuthContext
from shared.ui.base_gui import BaseGUI
from shared.ui.components import ActionButtonsComponent
from shared.ui.styles import COLORS, FONTS, LABEL_SIZES, WINDOW_SIZES
from user.application.authenticate_user_use_case import AuthenticateUserInputDto
from user.domain.user import User
from user.domain.user_role import UserRole
from user.ui.create_user_gui import CreateUserGUI


class AuthenticateGUI(BaseGUI):
    def __init__(self, use_cases=None, navigator=None):
        super().__init__(
            title="Login",
            size=WINDOW_SIZES["SQUARE_PANEL"],
            use_cases=use_cases,
            navigator=navigator,
        )

        self.roles = [role.value for role in UserRole]

        self.action_buttons = ActionButtonsComponent([
            {
                "text": "Login",
                "font": FONTS["PRIMARY_BUTTON"],
                "key": "-LOGIN-",
                "button_color": (COLORS["dark"], COLORS["secondary"]),
            },
            {
                "text": "Create User",
                "font": FONTS["SECONDARY_BUTTON"],
                "key": "-CREATE_USER-",
                "button_color": (COLORS["white"], COLORS["primary"]),
            },
        ])

        self.event_map = {
            "-LOGIN-": self._handle_user_login,
            "-CREATE_USER-": self._handle_create_user,
        }

    def create_layout(self):
        labels = [
            [
                sg.Text(
                    "Email",
                    font=FONTS["LABEL"],
                    size=LABEL_SIZES["DEFAULT"],
                    pad=(0, 10),
                )
            ],
            [
                sg.Text(
                    "Password",
                    font=FONTS["LABEL"],
                    size=LABEL_SIZES["DEFAULT"],
                    pad=(0, 10),
                )
            ],
            [
                sg.Text(
                    "Role",
                    font=FONTS["LABEL"],
                    size=LABEL_SIZES["DEFAULT"],
                    pad=(0, 10),
                )
            ],
        ]

        inputs = [
            [
                sg.Input(
                    key="-EMAIL-",
                    tooltip="Enter your email (e.g., user@email.com)",
                    pad=(0, 10),
                    font=FONTS["INPUT"],
                )
            ],
            [
                sg.Input(
                    key="-PASSWORD-",
                    password_char="*",
                    tooltip="Enter your password",
                    pad=(0, 10),
                    font=FONTS["INPUT"],
                )
            ],
            [
                sg.Combo(
                    self.roles,
                    default_value=self.roles[0],
                    key="-ROLE-",
                    readonly=True,
                    tooltip="Select your role in the system",
                    pad=(0, 10),
                    font=FONTS["INPUT"],
                )
            ],
        ]

        layout = [
            [
                sg.Image(
                    filename=os.path.join("assets", "png", "festum_logo_325x320.png"),
                    subsample=2,
                    pad=(5),
                )
            ],
            [
                sg.Text(
                    "WELCOME AGAIN!",
                    font=FONTS["TITLE_MAIN"],
                    justification="center",
                    pad=(1, 0),
                ),
                sg.Image(
                    filename=os.path.join("assets", "png", "grin_32x32.png"),
                    pad=(1, 0),
                ),
            ],
            [
                sg.Text(
                    "Please log in to continue",
                    font=FONTS["SUBTITLE"],
                    justification="center",
                    pad=(20, 20),
                    text_color=COLORS["secondary"],
                )
            ],
            [
                sg.Column(
                    labels,
                    element_justification="right",
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
            self.show_success_popup(
                f"Welcome, {self.auth_context.name} ({self.auth_context.role.value})!"
            )

            if (
                self.auth_context.role.value == "CLIENT"
                or self.auth_context.role.value == "ORGANIZER"
            ):
                self.navigator.push_screen(
                    ListEventsGui, auth_context=self.auth_context
                )
            else:
                self.show_info_popup("Interface for STAFF are not implemented yet.")

        except Exception as e:
            self.show_error_popup(f"Error authenticating user: {e}")

    def _handle_create_user(self, values):
        self.navigator.push_screen(CreateUserGUI)

    def _set_auth_context(self, user: User):
        self.auth_context = AuthContext(
            id=user.id, name=user.name, email=user.email, role=user.role
        )
