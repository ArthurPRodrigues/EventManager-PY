from enum import Enum


class UserRole(str, Enum):
    CLIENT = "CLIENT"
    ORGANIZER = "ORGANIZER"
    STAFF = "STAFF"
