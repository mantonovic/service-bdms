# -*- coding: utf-8 -*-S


class BmsException(Exception):
    def __init__(self, message, code, data = None):
        super().__init__(message)
        self.code = code
        self.data = data


class ActionWrong(BmsException):
    def __init__(self):
        super().__init__("Server error", 'E-000')


class NotFound(BmsException):
    def __init__(self):
        super().__init__("Not found", 'E-050')


class ActionEmpty(BmsException):
    def __init__(self):
        super().__init__("Action empty", 'E-200')


class AuthenticationException(BmsException):
    def __init__(self):
        super().__init__("Authentication error", 'E-102')


class AuthorizationException(BmsException):
    def __init__(self):
        super().__init__("Authorization error", 'E-101')


class WorkgroupFreezed(BmsException):
    def __init__(self):
        super().__init__("Workgroup is freezed", 'E-103')


class PatchAttributeException(BmsException):
    def __init__(self, attribute):
        super().__init__(f"Attribute \"{attribute}\" unknown", 'E-201')


class MissingParameter(BmsException):
    def __init__(self, parameter):
        super().__init__(f"Missing parameter {parameter}", 'E-203')


class Locked(BmsException):
    def __init__(self, id, data):
        super().__init__(
            f"Borehole: '{id}' locked.",
            'E-900', data
        )