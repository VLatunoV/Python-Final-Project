class GeneralError(Exception):
    '''
    GeneralError
    +---PromotionError
    |   +---UnallowedValueError
    |   +---UnallowedTypeError
    +---ProductError
    '''
    pass

class PromotionError(GeneralError):
    pass

class UnallowedValueError(PromotionError):
    pass

class UnallowedTypeError(PromotionError):
    pass

class ProductError(GeneralError):
    pass