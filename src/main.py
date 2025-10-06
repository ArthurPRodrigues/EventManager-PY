from __future__ import annotations

from shared.composition_root import build_application
from shared.domain.auth_context import AuthContext
from shared.ui.navigation_manager import NavigationManager
from shared.ui.test_ticket_redeemption_gui import TestTicketRedemptionGUI
from user.domain.user_role import UserRole


# NOTE: This branch is for just testing the email service feature
def run() -> None:
    mocket_auth_context = AuthContext(
        1,
        "Davi Brito",
        "user@example.com",
        UserRole.CLIENT,
    )

    app = build_application()
    navigator = NavigationManager(app)
    navigator.push_screen(TestTicketRedemptionGUI, auth_context=mocket_auth_context)


if __name__ == "__main__":
    run()
