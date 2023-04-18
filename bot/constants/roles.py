from enum import Enum


class Roles(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
