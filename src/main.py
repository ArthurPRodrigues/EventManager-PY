from __future__ import annotations

from shared.composition_root import build_application
from user.infra.presentation.create_user_view import CreateUserView


def run() -> None:
    build_application()
    CreateUserView()


if __name__ == "__main__":
    run()
