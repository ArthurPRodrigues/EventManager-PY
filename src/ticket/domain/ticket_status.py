from enum import Enum


class TicketStatus(str, Enum):
    PENDING = "PENDING"
    VALIDATED = "VALIDATED"
