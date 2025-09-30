import os
from abc import ABC, abstractmethod

import FreeSimpleGUI as sg

from shared.infra.error_logger import log_error
from shared.ui.components.action_buttons_component import ActionButtonsComponent
from shared.ui.styles import BUTTON_SIZES, COLORS, FONTS

sg.theme_add_new(
    "FESTUMTheme",
    {
        "BACKGROUND": COLORS["primary"],
        "TEXT": COLORS["white"],
        "INPUT": COLORS["light"],
        "TEXT_INPUT": COLORS["black"],
        "BUTTON": (COLORS["white"], COLORS["primary_lighter"]),
        "SCROLL": COLORS["primary"],
        "PROGRESS": (COLORS["secondary"], COLORS["primary"]),
        "SLIDER_DEPTH": 0,
        "PROGRESS_DEPTH": 0,
        "BORDER": 0,
    },
)

sg.theme_add_new(
    "PopupTheme",
    {
        "BACKGROUND": COLORS["light"],
        "TEXT": COLORS["black"],
        "INPUT": COLORS["white"],
        "TEXT_INPUT": COLORS["black"],
        "BUTTON": (COLORS["white"], COLORS["primary_lighter"]),
        "SCROLL": COLORS["primary"],  # Same as FESTUMTheme
        "PROGRESS": (COLORS["secondary"], COLORS["primary"]),  # Same as FESTUMTheme
        "SLIDER_DEPTH": 0,  # Same as FESTUMTheme
        "PROGRESS_DEPTH": 0,  # Same as FESTUMTheme
        "BORDER": 0,  # Same as FESTUMTheme
    },
)


# TODO: Refactor success/warning/error popups, create a PopupConfig dataclass and implement a popup template method pattern
class BaseGUI(ABC):
    def __init__(
        self,
        title: str,
        size: tuple = (800, 600),
        use_cases=None,
        navigator=None,
        auth_context=None,
    ):
        self.window = None
        self.title = title
        self.size = size
        self.use_cases = use_cases
        self.navigator = navigator
        self.auth_context = auth_context
        self.event_map = {}
        sg.theme("FESTUMTheme")

    @abstractmethod
    def create_layout(self):
        """Each child screen must implement its specific layout"""
        pass

    @abstractmethod
    def handle_events(self, event, values):
        """Each child screen must implement its specific events"""
        pass

    def show(self):
        """Common method to show the screen"""
        layout = self.create_layout()
        self.window = sg.Window(
            self.title,
            layout,
            size=self.size,
            resizable=False,
            finalize=True,
            element_justification="center",
        )
        return self.run()

    def run(self):
        """Main loop common to all screens"""
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break
            elif event == "-BACK-":
                # Return False to indicate user wants to go back
                self.window.close()
                return False
            else:
                # Delegates specific events to the child screen
                self.handle_events(event, values)

        self.window.close()
        return True

    def close(self):
        """Common method to close"""
        if self.window:
            self.window.close()

    # TODO: Deprecate info popup in favor of success/warning popup
    def show_info_popup(self, message: str, title: str = "Info"):
        """Common helper method for info popups"""
        sg.popup(message, title=title)

    def show_success_popup(self, message: str, title: str = "Success"):
        """Common helper method for success popups"""
        current_theme = sg.theme()
        sg.theme("PopupTheme")

        layout = [
            [
                sg.Image(
                    filename=os.path.join("assets", "png", "badge-check.png"),
                    pad=((20, 0), (10, 20)),
                ),
                sg.Text(
                    message,
                    font=FONTS["POPUP_LABEL"],
                    justification="center",
                    auto_size_text=True,
                    pad=((10, 20), (10, 20)),
                ),
            ],
            [
                sg.Button(
                    "OK",
                    key="-YES-",
                    font=FONTS["PRIMARY_BUTTON"],
                    button_color=(COLORS["white"], COLORS["success"]),
                    size=BUTTON_SIZES["SMALL"],
                ),
            ],
        ]

        window = sg.Window(
            title,
            layout,
            modal=True,
            element_justification="center",
        )
        event, _ = window.read()
        window.close()

        sg.theme(current_theme)

        return event

    def show_warning_popup(self, message: str, title: str = "Warning"):
        """Common helper method for warning popups"""

        current_theme = sg.theme()
        sg.theme("PopupTheme")

        layout = [
            [
                sg.Image(
                    filename=os.path.join("assets", "png", "triangle-alert.png"),
                    pad=((20, 0), (10, 20)),
                ),
                sg.Text(
                    message,
                    font=FONTS["POPUP_LABEL"],
                    justification="center",
                    auto_size_text=True,
                    pad=((10, 20), (10, 20)),
                ),
            ],
            [
                sg.Button(
                    "OK",
                    key="-YES-",
                    font=FONTS["PRIMARY_BUTTON"],
                    button_color=(COLORS["white"], COLORS["warning"]),
                    size=BUTTON_SIZES["SMALL"],
                ),
            ],
        ]

        window = sg.Window(
            title,
            layout,
            modal=True,
            element_justification="center",
        )
        event, _ = window.read()
        window.close()

        sg.theme(current_theme)

        return event

    def show_confirmation_popup(self, message: str, title: str = "Confirmation"):
        """Common helper method for confirmation popups"""
        current_theme = sg.theme()
        sg.theme("PopupTheme")

        action_buttons = ActionButtonsComponent([
            {
                "text": "Yes",
                "key": "-YES-",
                "font": FONTS["PRIMARY_BUTTON"],
                "button_color": (COLORS["white"], COLORS["primary_lighter"]),
            },
            {
                "text": "No",
                "key": "-NO-",
                "font": FONTS["SECONDARY_BUTTON"],
                "button_color": (COLORS["dark"], COLORS["light"]),
            },
        ])

        layout = [
            [
                sg.Image(
                    filename=os.path.join("assets", "png", "circle-question-mark.png"),
                    pad=((20, 0), (10, 20)),
                ),
                sg.Text(
                    message,
                    font=FONTS["POPUP_LABEL"],
                    justification="center",
                    auto_size_text=True,
                    pad=((10, 20), (10, 20)),
                ),
            ],
            *action_buttons.create_layout(),
        ]

        window = sg.Window(
            title,
            layout,
            modal=True,
            element_justification="center",
        )

        event, _ = window.read()

        window.close()

        sg.theme(current_theme)

        return event == "-YES-"

    def show_error_popup(self, message: str, title: str = "Error"):
        """Common helper method for error popups with logging"""
        log_error(message, self.auth_context)

        current_theme = sg.theme()
        sg.theme("PopupTheme")

        layout = [
            [
                sg.Image(
                    filename=os.path.join("assets", "png", "circle-x.png"),
                    pad=((20, 0), (10, 20)),
                ),
                sg.Text(
                    message,
                    font=FONTS["POPUP_LABEL"],
                    justification="center",
                    auto_size_text=True,
                    pad=((10, 20), (10, 20)),
                ),
            ],
            [
                sg.Button(
                    "OK",
                    key="-YES-",
                    font=FONTS["PRIMARY_BUTTON"],
                    button_color=(COLORS["white"], COLORS["error"]),
                    size=BUTTON_SIZES["SMALL"],
                ),
            ],
        ]

        window = sg.Window(
            title,
            layout,
            modal=True,
            element_justification="center",
        )
        event, _ = window.read()
        window.close()

        sg.theme(current_theme)

        return event

    def show_input_dialog(
        self,
        dialog_title: str,
        instruction_label: str,
        input_tooltip: str = "",
        confirm_button: str = "Confirm",
        cancel_button: str = "Cancel",
    ) -> tuple[bool, str]:
        """
        Shows a standardized input dialog with title, instruction, input field and buttons
        Returns: (was_confirmed, input_value)
        """

        current_theme = sg.theme()
        sg.theme("PopupTheme")

        action_buttons = ActionButtonsComponent([
            {
                "text": confirm_button,
                "key": "-CONFIRM-",
                "font": FONTS["PRIMARY_BUTTON"],
                "button_color": (COLORS["white"], COLORS["primary_lighter"]),
            },
            {
                "text": cancel_button,
                "key": "-CANCEL-",
                "font": FONTS["SECONDARY_BUTTON"],
                "button_color": (COLORS["dark"], COLORS["light"]),
            },
        ])

        layout = [
            [
                sg.Image(
                    filename=os.path.join("assets", "png", "square-pen.png"),
                    pad=((20, 0), (10, 20)),
                ),
                sg.Text(
                    instruction_label,
                    font=FONTS["POPUP_LABEL"],
                    justification="center",
                    auto_size_text=True,
                    pad=((10, 20), (10, 20)),
                ),
            ],
            [
                sg.Input(
                    key="-INPUT-",
                    tooltip=input_tooltip,
                    pad=(30, 10),
                    focus=True,
                    font=FONTS["LARGE_INPUT"],
                    background_color=COLORS["white"],
                    size=(25, 1),
                    justification="center",
                )
            ],
            *action_buttons.create_layout(),
        ]

        window = sg.Window(
            dialog_title,
            layout,
            modal=True,
            finalize=True,
            element_justification="center",
        )

        result = False
        input_value = ""

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, "-CANCEL-"):
                result = False
                break
            elif event == "-CONFIRM-":
                result = True
                input_value = values["-INPUT-"].strip()
                break

        window.close()

        sg.theme(current_theme)

        return result, input_value
