import os
import threading

import FreeSimpleGUI as sg

from shared.ui.base_gui import BaseGUI
from shared.ui.components.action_buttons_component import ActionButtonsComponent
from shared.ui.components.header_component import HeaderComponent
from shared.ui.styles import BUTTON_SIZES, COLORS, FONTS, WINDOW_SIZES


class TestTicketRedemptionGUI(BaseGUI):
    def __init__(self, use_cases=None, navigator=None, auth_context=None):
        super().__init__(
            title="Ticket Redemption",
            size=WINDOW_SIZES["SQUARE_WIDGET"],
            use_cases=use_cases,
            navigator=navigator,
            auth_context=auth_context,
        )

        self.header = HeaderComponent()

        self.action_buttons = ActionButtonsComponent([
            {
                "text": "Redeem Ticket",
                "key": "-REDEEM-",
                "font": FONTS["PRIMARY_BUTTON"],
                "size": BUTTON_SIZES["EXTRA_LARGE"],
                "button_color": (COLORS["dark"], COLORS["secondary"]),
            },
        ])

        self.event_map = {
            "-REDEEM-": self._handle_redeem_ticket,
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
                    "TICKET REDEMPTION",
                    font=FONTS["TITLE_MAIN"],
                    justification="center",
                    pad=((0, 0), (0, 10)),
                ),
            ],
            [
                sg.Text(
                    "Press the button to enter the\n 6-digit ticket code and start the redemption.",
                    font=FONTS["SUBTITLE"],
                    justification="center",
                    text_color=COLORS["secondary"],
                ),
            ],
        ]

        layout = [
            *self.header.create_layout(),
            [
                sg.Column(content_column, element_justification="center", pad=(0, 20)),
            ],
            *self.action_buttons.create_layout(),
            [
                sg.Text(
                    "We'll send you a confirmation email! =)",
                    font=FONTS["FOOTNOTE"],
                    justification="center",
                    text_color=COLORS["info"],
                    pad=(0, 10),
                ),
            ],
        ]
        return layout

    def handle_events(self, event, values):
        handler = self.event_map.get(event)
        if handler:
            handler(values)

    # NOTE: Clean Architecture VIOLATION
    # I'm calling the SmtpEmailService directly here to validate the ticket
    def _handle_redeem_ticket(self, _):
        confirmed, ticket_code = self.show_input_dialog(
            dialog_title="Redeem Ticket",
            instruction_label="Enter Ticket ID",
            input_tooltip="Enter the ID of the ticket you want to redeem (e.g., ABC123)",
            confirm_button="Redeem",
            cancel_button="Cancel",
        )

        if confirmed:
            if not ticket_code:
                self.show_warning_popup("Ticket ID cannot be empty.")
                return

            def send_email():
                try:
                    html_content = self.use_cases.html_template_engine.render(
                        template_name="redeem_ticket.html",
                        context={
                            "ticket_code": ticket_code,
                            "user_name": self.auth_context.name,
                        },
                    )

                    self.use_cases.smtp_email_service.send_email(
                        to=self.auth_context.email,
                        subject="Ticket Redeemed",
                        body=html_content,
                    )
                except Exception as e:
                    self.email_error = str(e)

            # Start email sending in background thread
            self.email_error = None
            email_thread = threading.Thread(target=send_email, daemon=True)
            email_thread.start()

            self.show_animated_wait_popup(
                gif_path=os.path.join("assets", "gifs", "sending_email.gif"),
                message="A confirmation email is being sent!",
                thread_to_wait_for=email_thread,
            )

            # Wait for thread to complete
            email_thread.join(timeout=5)

            if self.email_error:
                self.show_error_popup(f"Error validating ticket: {self.email_error}")
            else:
                self.show_success_popup(
                    f"Ticket '{ticket_code}' redeemed successfully! \n Check your email for confirmation."
                )
