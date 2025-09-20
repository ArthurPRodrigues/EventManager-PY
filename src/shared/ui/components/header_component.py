from typing import Any, Dict, Optional

import FreeSimpleGUI as sg


class HeaderComponent:
    def __init__(
        self,
        title: str,
        back_button: bool = True,
        extra_button: Optional[Dict[str, Any]] = None,
    ):
        self.title = title
        self.back_button = back_button
        self.extra_button = extra_button

    def create_layout(self):
        elements = []

        if self.back_button:
            elements.append(sg.Button("Back", key="-BACK-", size=(8, 1)))
            elements.append(sg.Push())

        elements.extend(
            [
                sg.Text(
                    self.title,
                    font=("Arial", 16, "bold"),
                    justification="center",
                ),
                sg.Push(),
            ]
        )

        if self.extra_button:
            elements.append(
                sg.Button(
                    self.extra_button["text"],
                    key=self.extra_button["key"],
                    size=self.extra_button.get("size", (12, 1)),
                )
            )

        return [elements]
