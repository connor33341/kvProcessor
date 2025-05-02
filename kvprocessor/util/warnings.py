import warnings

def deprecated(func):
    def wrapper(*args, **kwargs):
        warnings.warn(f"{func.__name__} is deprecated and will be removed in a future version.", 
                      DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)
    return wrapper

def ignore_warnings(func):
    """
    Decorator to ignore warnings in a function.

    Args:
        func (callable): The function to decorate.

    Returns:
        callable: The decorated function.
    """
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return func(*args, **kwargs)
    return wrapper