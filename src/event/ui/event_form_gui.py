import os
from datetime import datetime

import FreeSimpleGUI as sg

from event.application.create_event_use_case import CreateEventInputDto
from event.application.update_event_use_case import UpdateEventInputDto
from shared.ui import BaseGUI
from shared.ui.components.action_buttons_component import ActionButtonsComponent
from shared.ui.components.header_component import HeaderComponent
from shared.ui.styles import COLORS, FONTS, LABEL_SIZES, WINDOW_SIZES


class EventFormGUI(BaseGUI):
    def __init__(
        self,
        use_cases=None,
        navigator=None,
        auth_context=None,
        operation=None,
        event=None,
    ):
        super().__init__(
            title="Event Form",
            size=WINDOW_SIZES["SQUARE_PANEL"],
            use_cases=use_cases,
            navigator=navigator,
            auth_context=auth_context,
        )

        self.operation = operation
        self.event_id = event[0] if event else None
        self.event = event

        self.header = HeaderComponent()

        if operation == "CREATE":
            self.action_buttons = ActionButtonsComponent([
                {
                    "text": "Create Event",
                    "key": "-CREATE-",
                    "font": FONTS["PRIMARY_BUTTON"],
                    "button_color": (COLORS["dark"], COLORS["secondary"]),
                },
            ])

            self.event_map = {
                "-CREATE-": self._handle_create_event,
            }
        else:
            self.action_buttons = ActionButtonsComponent([
                {  # TODO: INSERIR BOTÃO MANAGE STAFF CONFORME DEFINIDO NO PROTÓTIPO
                    "text": "Update Event",
                    "key": "-UPDATE-",
                    "font": FONTS["PRIMARY_BUTTON"],
                    "button_color": (COLORS["dark"], COLORS["secondary"]),
                },
            ])

            self.event_map = {
                "-UPDATE-": self._handle_update_event,
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
                    "Start Date*",
                    font=FONTS["LABEL"],
                    size=LABEL_SIZES["DEFAULT"],
                    pad=(0, 10),
                ),
            ],
            [
                sg.Text(
                    "End Date*",
                    font=FONTS["LABEL"],
                    size=LABEL_SIZES["DEFAULT"],
                    pad=(0, 10),
                ),
            ],
            [
                sg.Text(
                    "Location*",
                    font=FONTS["LABEL"],
                    size=LABEL_SIZES["DEFAULT"],
                    pad=(0, 10),
                ),
            ],
            [
                sg.Text(
                    "Tickets*",
                    font=FONTS["LABEL"],
                    size=LABEL_SIZES["DEFAULT"],
                    pad=(0, 10),
                ),
            ],
        ]

        if self.operation == "UPDATE" and self.event:
            inputs = [
                [
                    sg.Input(
                        default_text=self.event[1],
                        key="-NAME-",
                        tooltip="Enter the event name",
                        font=FONTS["INPUT"],
                        pad=(0, 10),
                    ),
                ],
                [
                    sg.Input(
                        default_text=datetime.fromisoformat(self.event[3]).strftime(
                            "%d/%m/%Y %Hh%M"
                        ),
                        key="-START_DATE-",
                        tooltip="Enter the event's starting date in the format DD/MM/YYYY HHhMM",
                        font=FONTS["INPUT"],
                        pad=(0, 10),
                    ),
                ],
                [
                    sg.Input(
                        default_text=datetime.fromisoformat(self.event[4]).strftime(
                            "%d/%m/%Y %Hh%M"
                        ),
                        key="-END_DATE-",
                        tooltip="Enter the event's ending date in the format DD/MM/YYYY HHhMM",
                        font=FONTS["INPUT"],
                        pad=(0, 10),
                    ),
                ],
                [
                    sg.Input(
                        default_text=self.event[5],
                        key="-LOCATION-",
                        tooltip="Enter the event's location",
                        font=FONTS["INPUT"],
                        pad=(0, 10),
                    ),
                ],
                [
                    sg.Input(
                        default_text=self.event[6],
                        key="-MAX_TICKETS-",
                        tooltip="Enter the event's max ticket quantity",
                        font=FONTS["INPUT"],
                        pad=(0, 10),
                    ),
                ],
            ]
        else:
            inputs = [
                [
                    sg.Input(
                        key="-NAME-",
                        tooltip="Enter the event name",
                        font=FONTS["INPUT"],
                        pad=(0, 10),
                    ),
                ],
                [
                    sg.Input(
                        key="-START_DATE-",
                        tooltip="Enter the event's starting date in the format DD/MM/YYYY HHhMM",
                        font=FONTS["INPUT"],
                        pad=(0, 10),
                    ),
                ],
                [
                    sg.Input(
                        key="-END_DATE-",
                        tooltip="Enter the event's ending date in the format DD/MM/YYYY HHhMM",
                        font=FONTS["INPUT"],
                        pad=(0, 10),
                    ),
                ],
                [
                    sg.Input(
                        key="-LOCATION-",
                        tooltip="Enter the event's location",
                        font=FONTS["INPUT"],
                        pad=(0, 10),
                    ),
                ],
                [
                    sg.Input(
                        key="-MAX_TICKETS-",
                        tooltip="Enter the event's max ticket quantity",
                        font=FONTS["INPUT"],
                        pad=(0, 10),
                    ),
                ],
            ]

        if self.operation == "CREATE":
            layout = [
                *self.header.create_layout(),
                [
                    sg.Text(
                        "CREATE YOUR EVENT",
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
                        "Create an event.",
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
        else:
            layout = [
                *self.header.create_layout(),
                [
                    sg.Text(
                        "UPDATE YOUR EVENT",
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
                        "Update an existing event.",
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

    def _handle_create_event(self, values):
        if self._check_filled_fields(values) is True:
            name = values.get("-NAME-")
            start_date = values.get("-START_DATE-")
            end_date = values.get("-END_DATE-")
            location = values.get("-LOCATION-")
            max_tickets = values.get("-MAX_TICKETS-")

            try:
                input_dto = CreateEventInputDto(
                    name=name,
                    start_date=datetime.strptime(start_date, "%d/%m/%Y %Hh%M"),
                    end_date=datetime.strptime(end_date, "%d/%m/%Y %Hh%M"),
                    location=location,
                    max_tickets=int(max_tickets),
                    organizer_id=self.auth_context.id,
                )

                event = self.use_cases.create_event_use_case.create_event(input_dto)

                self.show_success_popup(f"Event {event.name} created successfully!")

                self.navigator.pop_screen()

            except Exception as e:
                self.show_error_popup(f"Error creating event: {e!s}")

    def _handle_update_event(self, values):
        if self._check_filled_fields(values) is True:
            name = values.get("-NAME-")
            start_date = values.get("-START_DATE-")
            end_date = values.get("-END_DATE-")
            location = values.get("-LOCATION-")
            max_tickets = values.get("-MAX_TICKETS-")

            try:
                input_dto = UpdateEventInputDto(
                    event_id=self.event[0],
                    name=name,
                    start_date=datetime.strptime(start_date, "%d/%m/%Y %Hh%M"),
                    end_date=datetime.strptime(end_date, "%d/%m/%Y %Hh%M"),
                    location=location,
                    max_tickets=int(max_tickets),
                    organizer_id=self.auth_context.id,
                )

                updated_event = self.use_cases.update_event_use_case.execute(input_dto)

                self.show_success_popup(
                    f"Event {updated_event.name} updated successfully!"
                )

                self.navigator.pop_screen()

            except Exception as e:
                self.show_error_popup(f"Error updating event: {e!s}")

    def _check_filled_fields(self, values):
        name = values.get("-NAME-")
        start_date = values.get("-START_DATE-")
        end_date = values.get("-END_DATE-")
        location = values.get("-LOCATION-")
        max_tickets = values.get("-MAX_TICKETS-")

        if (
            not name
            or not start_date
            or not end_date
            or not location
            or not max_tickets
        ):
            self.show_warning_popup("Please fill all fields")
            return
        else:
            return True
