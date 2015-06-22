class GeneralError(Exception):
    '''
    GeneralError
    +---PromotionError
    |   +---UnallowedValueError
    |   +---UnallowedTypeError
    +---UserError
    |   +---EmptyStringError
    +---ProductError
    |   +---IncorrectTypeError
    +---ProductManagerError
    |   +---FailedToLoadError
    '''
    pass

class PromotionError(GeneralError):
    pass

class UnallowedValueError(PromotionError):
    pass

class UnallowedTypeError(PromotionError):
    pass

class UserError(GeneralError):
    pass

class EmptyStringError(UserError):
    pass

class ProductError(GeneralError):
    pass

class IncorrectTypeError(ProductError):
    pass

class ProductManagerError(GeneralError):
    pass

class FailedToLoadError(ProductManagerError):
    pass
