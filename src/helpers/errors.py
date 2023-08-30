class AccessDenied(PermissionError):
    pass

class DuplicateEntry(ValueError):
    pass

class AuthenticationError(ValueError):
    pass