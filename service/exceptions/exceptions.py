from typing import Optional


class ENIDBaseError(Exception):
    def __init__(self, message: Optional[str] = None):
        self.message = message

class ENIDBirthDateDecodeError(ENIDBaseError):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message=message)

class ENIDDecodeError(ENIDBaseError):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message)

class ENIDCenturyDecodeError(ENIDBaseError):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message)

class ENIDGovernorateDecodeError(ENIDBaseError):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message)