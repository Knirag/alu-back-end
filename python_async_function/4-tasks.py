#!/usr/bin/env python3
"""Creates and returns an asyncio.Task that waits for a random delay between 0 and max_delay seconds."""
import asyncio
import random
from typing import List
task_wait_random = __import__('3-tasks').wait_random


async def task_wait_n(n: int = 0, max_delay: int = 10) -> List[float]:
    """
    Creates and returns an asyncio.Task that waits for a random delay between 0 and max_delay seconds.

    Parameters:
      - max_delay (int): The maximum delay in seconds.

    Returns:
      - asyncio.Task: A Task representing the execution of wait_n.
    """

    delays: List[float] = []
    tasks: List[asyncio.Task] = []

    for _ in range(n):
        tasks.append(task_wait_random(max_delay))

    for task in asyncio.as_completed((tasks)):
        delay = await task
        delays.append(delay)

    return delays