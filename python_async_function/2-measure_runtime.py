#!/usr/bin/env python3
"""Measures the total execution time for wait_n(n, max_delay) and returns total_time"""
import asyncio
import time
from typing import List
wait_n = __import__('1-concurrent_coroutines').wait_n
def measure_time(n: int, max_delay: int) -> float:
    """

    Parameters:
      - n (int): The number of times to call wait_n.
      - max_delay (int): The maximum delay in seconds for each wait_random call.

    Returns:
      - float: The average execution time per call.
    """
    start_time = time.time()
    asyncio.run(wait_n(n, max_delay))
    end_time = time.time()

    total_time = end_time - start_time
    average_time_per_call = total_time / n
    return average_time_per_call

# Example usage:
if __name__ == "__main__":
    n = 5
    max_delay = 9
    print(measure_time(n, max_delay))
