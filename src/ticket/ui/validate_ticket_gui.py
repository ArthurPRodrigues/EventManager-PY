import os

import FreeSimpleGUI as sg

from shared.ui.base_gui import BaseGUI
from shared.ui.components.action_buttons_component import ActionButtonsComponent
from shared.ui.components.header_component import HeaderComponent
from shared.ui.styles import BUTTON_SIZES, COLORS, FONTS, WINDOW_SIZES
from ticket.application.dtos import ValidateTicketInputDto


class ValidateTicketGUI(BaseGUI):
    def __init__(self, use_cases=None, navigator=None, auth_context=None):
        super().__init__(
            title="Validate Ticket",
            size=WINDOW_SIZES["SQUARE_WIDGET"],
            use_cases=use_cases,
            navigator=navigator,
            auth_context=auth_context,
        )

        self.header = HeaderComponent()

        self.action_buttons = ActionButtonsComponent([
            {
                "text": "Validate Ticket",
                "key": "-VALIDATE-",
                "font": FONTS["PRIMARY_BUTTON"],
                "size": BUTTON_SIZES["EXTRA_LARGE"],
                "button_color": (COLORS["dark"], COLORS["secondary"]),
            },
        ])

        self.event_map = {
            "-VALIDATE-": self._handle_validate_ticket,
        }

    def create_layout(self):
        content_column = [
            [
                sg.Image(
                    filename=os.path.join("assets", "png", "ticket.png"),
                    pad=((0, 0), (0, 15)),
                )
            ],
            [
                sg.Text(
                    "TICKET VALIDATION",
                    font=FONTS["TITLE_MAIN"],
                    justification="center",
                    pad=((0, 0), (0, 10)),
                ),
            ],
            [
                sg.Text(
                    "Press the button to enter the\n 6-digit ticket code and start the validation.",
                    font=FONTS["SUBTITLE"],
                    justification="center",
                    text_color=COLORS["secondary"],
                )
            ],
        ]

        layout = [
            *self.header.create_layout(),
            [
                sg.Column(content_column, element_justification="center", pad=(0, 40)),
            ],
            *self.action_buttons.create_layout(),
        ]
        return layout

    def handle_events(self, event, values):
        handler = self.event_map.get(event)
        if handler:
            handler(values)

    def _handle_validate_ticket(self, _):
        confirmed, ticket_code = self.show_input_dialog(
            dialog_title="Validate Ticket",
            instruction_label="Enter Ticket ID",
            input_tooltip="Enter the ID of the ticket you want to validate (e.g., ABC123)",
            confirm_button="Validate",
            cancel_button="Cancel",
        )

        if confirmed:
            if not ticket_code:
                self.show_warning_popup("Ticket ID cannot be empty.")
                return

            if self.auth_context.role.value == "ORGANIZER":
                try:
                    input_dto = ValidateTicketInputDto(
                        user_id=self.auth_context.id,
                        user_role=self.auth_context.role,
                        code=ticket_code.strip().upper(),
                    )
                    self.use_cases.validate_ticket_as_organizer_use_case.execute(
                        input_dto
                    )
                    self.show_info_popup(
                        f"Ticket '{ticket_code}' validated successfully!"
                    )
                except Exception as e:
                    self.show_error_popup(f"Error validating ticket: {e!s}")

            elif self.auth_context.role.value == "STAFF":
                try:
                    input_dto = ValidateTicketInputDto(
                        user_id=self.auth_context.id,
                        user_role=self.auth_context.role,
                        code=ticket_code.strip().upper(),
                    )
                    self.use_cases.validate_ticket_as_staff_use_case.execute(input_dto)
                    self.show_info_popup(
                        f"Ticket '{ticket_code}' validated successfully!"
                    )
                except Exception as e:
                    self.show_error_popup(f"Error validating ticket: {e!s}")
