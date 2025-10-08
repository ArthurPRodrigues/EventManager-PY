import FreeSimpleGUI as sg

from event.infra.ai.gemini_service import GeminiService
from shared.ui.base_gui import BaseGUI
from shared.ui.components import ActionButtonsComponent, HeaderComponent
from shared.ui.styles import COLORS, FONTS, LABEL_SIZES, WINDOW_SIZES


class CreateEventMockGUI(BaseGUI):
    def __init__(self, use_cases=None, navigator=None, auth_context=None):
        super().__init__(
            "Create Event (Mock)",
            WINDOW_SIZES["HORIZONTAL_DEFAULT"],
            use_cases,
            navigator,
            auth_context,
        )

        try:
            self.gemini_service = GeminiService()
        except ValueError as e:
            self.show_error_popup(str(e))
            self.gemini_service = None

        self.header = HeaderComponent()
        self.action_buttons = ActionButtonsComponent([
            {
                "text": "Create Event",
                "key": "-CREATE-",
                "font": FONTS["PRIMARY_BUTTON"],
            }
        ])
        self.event_map = {
            "-CREATE-": self._handle_create_event,
            "-GENERATE_DESC-": self._handle_generate_description,
        }
        self.event_types = ["Show", "Party", "Conference", "Workshop", "Other"]

    def create_layout(self):
        labels = [
            [
                sg.Text(
                    "Event Name",
                    font=FONTS["LABEL"],
                    size=LABEL_SIZES["DEFAULT"],
                    pad=(0, 10),
                )
            ],
            [
                sg.Text(
                    "Event Type",
                    font=FONTS["LABEL"],
                    size=LABEL_SIZES["DEFAULT"],
                    pad=(0, 10),
                )
            ],
            [
                sg.Text(
                    "Keywords",
                    font=FONTS["LABEL"],
                    size=LABEL_SIZES["DEFAULT"],
                    pad=(0, 10),
                )
            ],
            [
                sg.Text(
                    "Description",
                    font=FONTS["LABEL"],
                    size=LABEL_SIZES["DEFAULT"],
                    pad=(0, 10),
                )
            ],
        ]

        inputs = [
            [
                sg.Input(
                    key="-EVENT_NAME-",
                    tooltip="Enter the event name",
                    font=FONTS["INPUT"],
                    pad=(0, 10),
                    expand_x=True,
                )
            ],
            [
                sg.Combo(
                    self.event_types,
                    default_value=self.event_types[0],
                    key="-EVENT_TYPE-",
                    readonly=True,
                    font=FONTS["INPUT"],
                    pad=(0, 10),
                    expand_x=True,
                )
            ],
            [
                sg.Input(
                    key="-EVENT_KEYWORDS-",
                    tooltip="Enter keywords separated by commas",
                    font=FONTS["INPUT"],
                    pad=(0, 10),
                    expand_x=True,
                )
            ],
            [
                sg.Multiline(
                    "",
                    key="-DESCRIPTION-",
                    font=FONTS["INPUT"],
                    background_color=COLORS["light"],
                    text_color=COLORS["black"],
                    pad=(0, 10),
                    size=(None, 3),
                    expand_x=True,
                )
            ],
            [
                sg.Push(),
                sg.Button(
                    "Generate Description with AI ✨",
                    key="-GENERATE_DESC-",
                    font=FONTS["BUTTON"],
                    button_color=(COLORS["dark"], COLORS["secondary"]),
                    pad=(0, 15),
                ),
            ],
        ]

        layout = [
            *self.header.create_layout(),
            [
                sg.Text(
                    "Create New Event",
                    font=FONTS["TITLE_MAIN"],
                    justification="center",
                    pad=(0, 10),
                )
            ],
            [
                sg.Column(
                    labels,
                    element_justification="left",
                    vertical_alignment="top",
                    pad=(30, 0),
                    expand_x=True,
                ),
                sg.Column(
                    inputs,
                    element_justification="left",
                    vertical_alignment="top",
                    pad=((0, 30), (0, 0)),
                    expand_x=True,
                ),
            ],
            *self.action_buttons.create_layout(),
        ]

        return layout

    def handle_events(self, event, values):
        handler = self.event_map.get(event)
        if handler:
            handler(values)

    def _handle_generate_description(self, values):
        if not self.gemini_service:
            return self.show_error_popup("AI service is not working. Try again later.")

        event_name = values["-EVENT_NAME-"]
        event_type = values["-EVENT_TYPE-"]
        event_keywords = values["-EVENT_KEYWORDS-"]

        if not event_name or not event_type or not event_keywords:
            return self.show_error_popup(
                "Please fill in all fields to generate the description."
            )

        self.window["-DESCRIPTION-"].update("Generating description... Please wait.")
        self.window.refresh()

        description = self.gemini_service.generate_event_description(
            event_name, event_type, event_keywords
        )

        self.window["-DESCRIPTION-"].update(description)

    def _handle_create_event(self, values):
        self.show_info_popup("This feature is a work in progress.")
