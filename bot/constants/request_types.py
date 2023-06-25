from enum import Enum


class RequestTypes(str, Enum):
    FEEDBACK = "feedback"
    REGISTER = "register"
