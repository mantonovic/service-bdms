# -*- coding: utf-8 -*-S


class BmsException(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


class ActionEmpty(BmsException):
    def __init__(self):
        super().__init__("Action empty", 200)


class AuthenticationException(BmsException):
    def __init__(self):
        super().__init__("Authentication error", 102)


class AuthorizationException(BmsException):
    def __init__(self):
        super().__init__("Authorization error", 101)


class PatchAttributeException(BmsException):
    def __init__(self, attribute):
        super().__init__("Attribute \"%s\" unknown" % attribute, 201)
