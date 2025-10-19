from __future__ import annotations

import os
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import FreeSimpleGUI as sg

from shared.infra.error_logger import log_error
from shared.ui.components.action_buttons_component import ActionButtonsComponent
from shared.ui.styles import (
    BUTTON_SIZES,
    COLORS,
    FONTS,
)

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


@dataclass
class PopupConfig:
    title: str
    message: str
    icon_path: str | None = None
    buttons: list[dict[str, Any]] = field(default_factory=list)
    modal: bool = True
    theme: str = "PopupTheme"


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

    def _show_popup_template(
        self, config: PopupConfig
    ) -> tuple[str | None, dict | None]:
        """Template method to show a popup based on a configuration."""
        current_theme = sg.theme()
        sg.theme(config.theme)

        top_row = []
        if config.icon_path:
            top_row.append(
                sg.Image(
                    filename=config.icon_path,
                    pad=((20, 0), (10, 20)),
                )
            )

        top_row.append(
            sg.Text(
                config.message,
                font=FONTS["POPUP_LABEL"],
                justification="center",
                auto_size_text=True,
                pad=((10, 20), (10, 20)),
            )
        )

        action_buttons = ActionButtonsComponent(config.buttons)

        layout = [top_row, *action_buttons.create_layout()]

        window = sg.Window(
            config.title,
            layout,
            modal=config.modal,
            element_justification="center",
        )
        event, values = window.read()
        window.close()

        sg.theme(current_theme)
        return event, values

    def show_success_popup(self, message: str, title: str = "Success"):
        """Common helper method for success popups"""
        config = PopupConfig(
            title=title,
            message=message,
            icon_path=os.path.join("assets", "png", "badge-check.png"),
            buttons=[
                {
                    "text": "OK",
                    "key": "-OK-",
                    "font": FONTS["PRIMARY_BUTTON"],
                    "button_color": (COLORS["white"], COLORS["success"]),
                    "size": BUTTON_SIZES["SMALL"],
                }
            ],
        )
        event, _ = self._show_popup_template(config)
        return event

    def show_warning_popup(self, message: str, title: str = "Warning"):
        """Common helper method for warning popups"""
        config = PopupConfig(
            title=title,
            message=message,
            icon_path=os.path.join("assets", "png", "triangle-alert.png"),
            buttons=[
                {
                    "text": "OK",
                    "key": "-OK-",
                    "font": FONTS["PRIMARY_BUTTON"],
                    "button_color": (COLORS["white"], COLORS["warning"]),
                    "size": BUTTON_SIZES["SMALL"],
                }
            ],
        )
        event, _ = self._show_popup_template(config)
        return event

    def show_error_popup(self, message: str, title: str = "Error"):
        """Common helper method for error popups with logging"""
        log_error(message, self.auth_context)

        config = PopupConfig(
            title=title,
            message=message,
            icon_path=os.path.join("assets", "png", "circle-x.png"),
            buttons=[
                {
                    "text": "OK",
                    "key": "-OK-",
                    "font": FONTS["PRIMARY_BUTTON"],
                    "button_color": (COLORS["white"], COLORS["error"]),
                    "size": BUTTON_SIZES["SMALL"],
                }
            ],
        )
        event, _ = self._show_popup_template(config)
        return event

    def show_confirmation_popup(self, message: str, title: str = "Confirmation"):
        """Common helper method for confirmation popups"""
        config = PopupConfig(
            title=title,
            message=message,
            icon_path=os.path.join("assets", "png", "circle-question-mark.png"),
            buttons=[
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
            ],
        )
        event, _ = self._show_popup_template(config)
        return event == "-YES-"

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

    def show_animated_wait_popup(
        self,
        gif_path: str,
        message: str,
        time_between_frames: int = 50,
        thread_to_wait_for: threading.Thread | None = None,
    ):
        """
        Shows an animated GIF popup window
        Args:
            gif_path: Path to the GIF file
            message: Message to display above the GIF
            time_between_frames: Time in milliseconds between animation frames
            thread_to_wait_for: Optional thread to wait for before closing the popup
        """

        current_theme = sg.theme()
        sg.theme("PopupTheme")

        popup_layout = [
            [
                sg.Text(
                    message,
                    font=("Montserrat", 14, "bold"),
                    justification="center",
                )
            ],
            [
                sg.Image(
                    filename=gif_path,
                    enable_events=True,
                    key="-IMAGE-",
                    pad=(0, 20),
                )
            ],
            [
                sg.Text(
                    "Please wait",
                    font=("Montserrat", 14),
                    justification="center",
                    text_color=COLORS["secondary_darker"],
                    key="-WAITING_TEXT-",
                )
            ],
        ]

        content = [
            [sg.VPush()],
            [
                sg.Column(
                    layout=popup_layout,
                    element_justification="center",
                    expand_x=True,
                    expand_y=True,
                    pad=(10, 20),
                )
            ],
            [sg.VPush()],
        ]

        layout = content

        window = sg.Window(
            "",
            layout,
            no_titlebar=True,
            grab_anywhere=True,
            keep_on_top=True,
            modal=True,
            finalize=True,
            element_justification="center",
        )

        dot_counter = 0

        while True:
            event, _ = window.read(timeout=100)

            if event == sg.WIN_CLOSED:
                break

            if thread_to_wait_for and not thread_to_wait_for.is_alive():
                break

            window["-IMAGE-"].update_animation_no_buffering(
                gif_path, time_between_frames=time_between_frames
            )

            dots = "." * dot_counter
            window["-WAITING_TEXT-"].update(value=f"Please wait{dots}")
            dot_counter = (dot_counter + 1) % 4

        window.close()

        sg.theme(current_theme)
