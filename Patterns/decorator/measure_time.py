def measure_time(function):
    """
    A simple decorator that measures and prints the execution time of a function.

    This decorator demonstrates the basic structure of the decorator pattern:
    1. Takes a function as an argument
    2. Defines a wrapper function that adds behavior
    3. Returns the wrapper function
    """

    def wrapper(*args, **kwargs):
        # Import time module inside the wrapper to avoid global import
        import time

        # Capture start time before function execution
        start = time.time()
        # Call the original function and store its result
        result = function(*args, **kwargs)
        # Calculate total execution time
        total = time.time() - start
        # Print the execution time
        print(total, 'seconds')
        # Return the original function's result
        return result

    # Return the wrapper function
    return wrapper


# Apply the measure_time decorator to the suma function
# This is equivalent to: suma = measure_time(suma)
@measure_time
def addition(a, b):
    # This function deliberately waits 0.5 seconds to demonstrate
    # the time measurement functionality
    import time
    time.sleep(0.5)
    return a + b


# Call the decorated function
# The decorator will measure and print the execution time
print(addition(10, 20))
