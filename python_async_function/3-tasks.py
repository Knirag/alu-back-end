#!/usr/bin/env python3
"""Creates and returns an asyncio.Task that waits for a random delay between 0 and max_delay seconds.
"""
import asyncio
wait_n = __import__('2-measure_runtime').wait_n
def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Parameters:
      - max_delay (int): The maximum delay in seconds.

    Returns:
      - asyncio.Task: A Task representing the execution of wait_random.
    """
    return asyncio.create_task(wait_n(1, max_delay))

# Example usage:
if __name__ == "__main__":
    async def test(max_delay: int):
        task = task_wait_random(max_delay)
        await task
        print(task.__class__)

    asyncio.run(test(5))

