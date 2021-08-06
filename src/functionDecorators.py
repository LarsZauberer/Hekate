import logging
import time
from functools import wraps

def tryFunc(originalFunction):
    """Creates a wrapper function that executes every function with a try
    statement.
    Args: originalFunction (function): The function it should execute in the try statement.
    """
    @wraps(originalFunction)
    def wrapperFunction(*args, **kwargs):
        log = logging.getLogger(str(originalFunction.__qualname__))
        try:
            start_time = time.time()
            result = originalFunction(*args, **kwargs)
            if time.time() - start_time > 5:
                log.warning(f"Function {str(originalFunction.__qualname__)} took longer than expected. Time took: {time.time() - start_time}")
            return result
        except Exception:
            log.exception(f"Error while executing function {str(originalFunction.__qualname__)}")
            exit("Error while Executing -> Exit with failure")
    return wrapperFunction