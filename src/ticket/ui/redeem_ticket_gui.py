import FreeSimpleGUI as sg

from shared.ui.base_gui import BaseGUI
from shared.ui.components.action_buttons_component import ActionButtonsComponent
from shared.ui.styles import BUTTON_SIZES, COLORS, FONTS, WINDOW_SIZES
from ticket.application.redeem_ticket_use_case import (
    RedeemTicketInputDto,
)


class RedeemTicketGUI(BaseGUI):
    def __init__(
        self,
        use_cases=None,
        navigator=None,
        auth_context=None,
        event_id: int | None = None,
        redeem_ticket_count: int | None = None,
        max_tickets: int | None = None,
        tickets_redeemed: int | None = None,
        send_email: bool | None = None,
    ):
        super().__init__(
            title="Redeem Ticket",
            size=WINDOW_SIZES["SQUARE_WIDGET"],
            use_cases=use_cases,
            navigator=navigator,
            auth_context=auth_context,
        )

        self.event_id = event_id
        self.redeem_ticket_count = redeem_ticket_count
        self.send_email = send_email
        self.max_tickets = max_tickets
        self.tickets_redeemed = tickets_redeemed

        self.event_map = {
            "-REDEEM-": self._handle_redeem_ticket,
            "-CANCEL-": self._handle_cancel,
        }

    def create_layout(self):
        max_count = max(1, (self.max_tickets - self.tickets_redeemed) or 1)
        content_column = (
            [
                sg.Text(
                    "How many tickets do you want?",
                    font=FONTS["SUBTITLE"],
                    justification="center",
                    text_color=COLORS["secondary"],
                )
            ],
        )

        spinner_row = [
            sg.Spin(
                values=[i for i in range(1, max_count)],
                initial_value=min(1, max_count + 1),
                key="-COUNT-",
                size=(4, 1),
                font=FONTS["INPUT"],
                enable_events=True,
                readonly=True,
            )
        ]

        email_row = [
            sg.Checkbox("Send to my e-mail", key="-SEND_EMAIL-", default=False)
        ]

        self.action_buttons = ActionButtonsComponent([
            {
                "text": "Redeem",
                "key": "-REDEEM-",
                "font": FONTS["PRIMARY_BUTTON"],
                "size": BUTTON_SIZES["EXTRA_LARGE"],
                "button_color": (COLORS["dark"], COLORS["secondary"]),
            },
            {
                "text": "Cancel",
                "key": "-CANCEL-",
                "font": FONTS["PRIMARY_BUTTON"],
                "size": BUTTON_SIZES["EXTRA_LARGE"],
                "button_color": (COLORS["dark"], COLORS["secondary"]),
            },
        ])

        layout = [
            *content_column,
            spinner_row,
            email_row,
            *self.action_buttons.create_layout(),
        ]

        return layout

    def handle_events(self, event, values):
        handler = self.event_map.get(event)
        if handler:
            handler(values)

    def _handle_redeem_ticket(self, values):
        send_email = bool(values.get("-SEND_EMAIL-", False))
        count = int(values.get("-COUNT-", 1))

        try:
            input_dto = RedeemTicketInputDto(
                event_id=self.event_id,
                client_id=self.auth_context.id,
                redeem_ticket_count=count,
                send_email=send_email,
            )
            self.use_cases.redeem_ticket_use_case.execute(input_dto)
            message = f"{count} ticket(s) were successfully redeemed!"
            if send_email:
                message += "\n\nA confirmation was also sent to your email."
            self.show_success_popup(message)

        except Exception as e:
            self.show_error_popup(f"Error redeeming ticket(s): {e}")

    def _handle_cancel(self, _values=None):
        try:
            if self.navigator:
                self.window.close()
                self.navigator.pop_screen()
            else:
                self.window.close()
        except Exception:
            self.window.close()
