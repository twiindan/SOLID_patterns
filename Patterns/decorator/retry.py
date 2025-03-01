def retry(times, exceptions):
    """
    Retry Decorator
    Retries the wrapped function/method `times` times if the exceptions listed
    in ``exceptions`` are thrown

    This is another example of a parametrized decorator that takes two arguments:
    :param times: The number of times to repeat the wrapped function/method
    :type times: Int
    :param exceptions: Lists of exceptions that trigger a retry attempt
    :type Exceptions: Tuple of Exceptions
    """

    # The outer function takes the decorator parameters
    def decorator(func):
        # The middle function takes the function to be decorated
        def function(*args, **kwargs):
            # Keep track of how many attempts have been made
            attempt = 0
            # Keep trying until we reach the maximum number of attempts
            while attempt < times:
                try:
                    # Try to execute the original function
                    return func(*args, **kwargs)
                except exceptions:
                    # If one of the specified exceptions occurs, print a message
                    # and increment the attempt counter
                    print(
                        'Exception thrown when attempting to run %s, attempt '
                        '%d of %d' % (func, attempt, times)
                    )
                    attempt += 1
            # If we've exhausted all retries, try one more time
            # This will either succeed or propagate the exception
            return func(*args, **kwargs)

        # NOTE: There's a bug here - the function is being called immediately
        # instead of being returned. It should be:
        # return function
        # Instead of:
        return function()

    # Return the decorator function
    return decorator


# Apply the retry decorator to foo1 function
# The function will be retried up to 3 times if it raises ValueError or TypeError
@retry(times=3, exceptions=(ValueError, TypeError))
def foo1():
    print('Some code here ....')
    print('Oh no, we have exception')
    # This will trigger the retry mechanism
    raise ValueError('Some error')


# Call the decorated function
# Due to the bug in the decorator, this actually doesn't call foo1 again
# but instead calls the result of the decorator's immediate execution of foo1
foo1()
