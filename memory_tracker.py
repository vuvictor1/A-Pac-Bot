import tracemalloc

def start_tracking():
    """Start tracking memory usage."""
    tracemalloc.start()

def stop_tracking():
    """Stop tracking memory usage."""
    tracemalloc.stop()

def get_memory_usage():
    """Get the current memory usage in kilobytes."""
    current, peak = tracemalloc.get_traced_memory()
    return current // 1024, peak // 1024