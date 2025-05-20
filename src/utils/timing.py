import time

def time_it(func):
    """Decorator to measure execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = (end_time - start_time) * 1000  # in milliseconds
        print(f"Function '{func.__name__}' executed in {elapsed_time:.4f} ms")
        return result, elapsed_time
    return wrapper
