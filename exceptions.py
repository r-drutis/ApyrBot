# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass

class UnknownEntryTypeError(Error):
    """Raised when the journal entry type cannot be determined"""
    pass

