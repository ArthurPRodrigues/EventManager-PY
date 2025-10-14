import FreeSimpleGUI as sg

from shared.ui.base_gui import BaseGUI
from shared.ui.components.action_buttons_component import ActionButtonsComponent
from shared.ui.components.header_component import HeaderComponent
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
        tickets_available: int | None = None,
        redeem_ticket_count: int | None = None,
        send_email: bool | None = None,
    ):
        super().__init__(
            title="Redeem Ticket",
            size=WINDOW_SIZES["SQUARE_WIDGET"],
            use_cases=use_cases,
            navigator=navigator,
            auth_context=auth_context,
        )

        self.header = HeaderComponent()

        self.event_id = event_id
        self.tickets_available = tickets_available
        self.redeem_ticket_count = redeem_ticket_count

        self.event_map = {
            "-REDEEM-": self._handle_redeem_ticket,
            "-CANCEL-": self._handle_back,
            "-BACK-": self._handle_back,
        }

    def create_layout(self):
        max_count = max(1, int(self.tickets_available or 1))
        content_column = (
            [
                sg.Text(
                    "Redeem Ticket",
                    font=FONTS["TITLE_MAIN"],
                    justification="center",
                    pad=((0, 0), (0, 10)),
                ),
            ],
            [
                sg.Text(
                    "How many tickets do you want to redeem?",
                    font=FONTS["SUBTITLE"],
                    justification="center",
                    text_color=COLORS["secondary"],
                )
            ],
        )

        spinner_row = [
            sg.Spin(
                values=[i for i in range(1, max_count + 1)],
                initial_value=min(1, max_count),
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
                "text": "Redeem Ticket",
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
            *self.header.create_layout(),
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
        try:
            count = int(values.get("-COUNT-", 1))
        except (TypeError, ValueError):
            self.show_warning_popup("Please choose a valid quantity.")
            return

        if count <= 0:
            self.show_warning_popup("Count must be greater than zero.")
            return

        if self.event_id is None:
            self.show_error_popup("Event not provided.")
            return

        if self.tickets_available is not None and count > int(self.tickets_available):
            self.show_warning_popup(
                f"Only {self.tickets_available} ticket(s) available for this event."
            )
            return

        try:
            input_dto = RedeemTicketInputDto(
                event_id=self.event_id,
                client_id=self.auth_context.id,
                redeem_ticket_count=count,
                send_email=send_email,
            )
            self.use_cases.redeem_ticket_use_case.execute(input_dto)
            if count > 1 and send_email:
                self.show_success_popup(f"{count} tickets were successfully redeemed!")
                self.show_success_popup(f"{count} tickets were sent to your email!")
            elif count > 1 and not send_email:
                self.show_success_popup(f"{count} tickets were successfully redeemed!")
            elif count == 1 and not send_email:
                self.show_success_popup("Ticket successfully redeemed!")
            else:
                self.show_success_popup("Ticket successfully redeemed!")
                self.show_success_popup("Ticket was sent to your email!")

        except Exception as e:
            self.show_error_popup(f"Error redeeming ticket(s): {e}")

    def _handle_back(self, _values=None):
        try:
            if self.navigator:
                self.window.close()
                self.navigator.pop_screen()
            else:
                self.window.close()
        except Exception:
            self.window.close()
