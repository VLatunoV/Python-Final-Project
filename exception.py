class GeneralError(Exception):
    '''
    GeneralError
    +---InvalidInputError
        +---IncorrectTypeError
        +---EmptyFieldError
        +---UnallowedValueError
    +---FailedFileOperationError
    '''
    pass

class InvalidInputError(GeneralError):
    pass

class IncorrectTypeError(InvalidInputError):
    pass

class EmptyFieldError(InvalidInputError):
    pass

class UnallowedValueError(InvalidInputError):
    pass

class FailedFileOperationError(GeneralError):
    pass
