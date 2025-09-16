from abc import ABC, abstractmethod

import FreeSimpleGUI as sg


class BaseGUI(ABC):
    def __init__(self, title: str, size: tuple = (800, 600), use_cases=None):
        self.window = None
        self.title = title
        self.size = size
        self.use_cases = use_cases
        self.event_map = {}
        sg.theme("Default1")

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
                self.show_info_popup("Voltando...")
                break
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
