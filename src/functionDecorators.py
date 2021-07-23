import logging
from functools import wraps

def tryFunc(originalFunction):
    """Creates a wrapper function that executes every function with a try
    statement.
    Args: originalFunction (function): The function it should execute in the try
        statement.
    """
    @wraps(originalFunction)
    def wrapperFunction(*args, **kwargs):
        log = logging.getLogger(str(originalFunction.__qualname__))
        try:
            return originalFunction(*args, **kwargs)
        except Exception:
            log.exception(f"Error while executing function {str(originalFunction.__qualname__)}")
            exit("Error while Executing -> Exit with failure")
    return wrapperFunction