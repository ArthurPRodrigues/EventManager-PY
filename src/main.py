from __future__ import annotations

from shared.composition_root import build_application
from shared.ui.navigation_manager import NavigationManager
from user.infra.presentation.create_user_gui import CreateUserGUI


def run() -> None:
    app = build_application()
    navigator = NavigationManager(app)
    navigator.push_screen(CreateUserGUI) 


if __name__ == "__main__":
    run()
