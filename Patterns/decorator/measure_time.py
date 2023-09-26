def measure_time(function):
    def wrapper(*args, **kwargs):
        import time

        start = time.time()
        result = function(*args, **kwargs)
        total = time.time() - start
        print(total, 'seconds')
        return result

    return wrapper


@measure_time
def suma(a, b):
    import time
    time.sleep(0.5)
    return a + b

print(suma(10, 20))