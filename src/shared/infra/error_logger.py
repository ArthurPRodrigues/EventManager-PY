import os
from datetime import UTC, datetime

from shared.domain.auth_context import AuthContext


def log_error(message: str, auth_context: AuthContext = None):
    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")

    user_email = auth_context.email if auth_context else "N/A"
    user_role = auth_context.role.value if auth_context else "N/A"
    user_info = f" - User: {user_email} ({user_role})"

    log_entry = f"[{timestamp}] ERROR: {message}{user_info}\n"

    with open("logs/errors.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)
