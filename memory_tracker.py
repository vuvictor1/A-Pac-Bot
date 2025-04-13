# File: memory_tracker.py
# Description: This file contains the memory tracking logic for the Pac-Bot game.
import tracemalloc

def start_tracking():  # Start tracking memory usage
    tracemalloc.start()


def stop_tracking(): # Stop tracking memory usage
    tracemalloc.stop()


def get_memory_usage(): # Get current memory usage
    current, peak = tracemalloc.get_traced_memory() 
    return current // 1024, peak // 1024 # Convert to KB
