from abc import ABC, abstractmethod

import FreeSimpleGUI as sg


class BaseGUI(ABC):
    def __init__(
        self, title: str, size: tuple = (800, 600), use_cases=None, navigator=None, auth_context=None,
    ):
        self.window = None
        self.title = title
        self.size = size
        self.use_cases = use_cases
        self.navigator = navigator
        self.auth_context = auth_context
        self.event_map = {}
        sg.theme("Reds")

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
            self.title, layout, size=self.size, resizable=True, finalize=True
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

    def show_info_popup(self, message: str, title: str = "Info"):
        """Common helper method for info popups"""
        sg.popup(message, title=title)

    def show_warning_popup(self, message: str, title: str = "Warning"):
        """Common helper method for warning popups"""
        sg.popup(message, title=title)

    def show_confirmation_popup(self, message: str, title: str = "Confirmation"):
        """Common helper method for confirmation popups"""
        result = sg.popup_yes_no(message, title=title)
        return result == "Yes"

    def show_error_popup(self, message: str, title: str = "Error"):
        """Common helper method for error popups"""
        sg.popup(message, title=title)

    def show_input_dialog(
        self,
        dialog_title: str,
        instruction_label: str,
        input_placeholder: str = "",
        confirm_button: str = "Confirm",
        cancel_button: str = "Cancel",
    ) -> tuple[bool, str]:
        """
        Shows a standardized input dialog with title, instruction, input field and buttons
        Returns: (was_confirmed, input_value)
        """
        layout = [
            [sg.Text(instruction_label, font=("Arial", 12), justification="center")],
            [
                sg.Input(
                    default_text=input_placeholder,
                    key="-INPUT-",
                    size=(40, 1),
                    focus=True,
                )
            ],
            [
                sg.Button(confirm_button, key="-CONFIRM-", size=(12, 1)),
                sg.Button(cancel_button, key="-CANCEL-", size=(12, 1)),
            ],
        ]

        dialog_window = sg.Window(
            dialog_title,
            layout,
            modal=True,
            finalize=True,
            element_justification="center",
        )

        result = False
        input_value = ""

        while True:
            event, values = dialog_window.read()

            if event in (sg.WIN_CLOSED, "-CANCEL-"):
                result = False
                break
            elif event == "-CONFIRM-":
                result = True
                input_value = values["-INPUT-"].strip()
                break

        dialog_window.close()
        return result, input_value
