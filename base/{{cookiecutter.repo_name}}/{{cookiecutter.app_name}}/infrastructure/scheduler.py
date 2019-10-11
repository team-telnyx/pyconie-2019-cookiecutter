import asyncio
import heapq
import time
from typing import Any, Callable, List, Mapping, Optional

import attr
from aiohttp import ClientSession

from {{cookiecutter.app_name}}.infrastructure.call_control import CallControl

_epsilon = 1e-6


@attr.s(slots=True, frozen=True)
class QueuedMessage:
    """Request with a timestamp"""

    ts = attr.ib()
    msg = attr.ib()

    # The comparison operators are necessary to determine priority
    def __lt__(self, other) -> bool:
        return self.ts < other.ts

    def __eq__(self, other) -> bool:
        return self.ts == other.ts


class UnifiedTimedQueue:
    """Stores items with timestamps in a priority queue.
    Fires the given handler whenever an item at the front of the queue
    is ready for processing.
    """

    def __init__(
        self, handler: CallControl, *, loop: asyncio.AbstractEventLoop = None
    ) -> None:
        self._queue: List[QueuedMessage] = []
        self._handler = handler
        self._task: Optional[asyncio.Future[None]] = None
        self._loop = loop or asyncio.get_event_loop()

    def __len__(self) -> int:
        return len(self._queue)

    async def _sleep_and_process(self, ts: float) -> None:
        """Sleep until the specified timestamp, then process items that are ready."""

        # If necessary, sleep until timestamp is reached.
        sleep_time = ts - time.time()
        if ts >= _epsilon:
            await asyncio.sleep(sleep_time)

        # Process all items that are ready (allowing a bit of wiggle room).
        cutoff = time.time() + _epsilon
        while self._queue and self._queue[0].ts < cutoff:
            qm = heapq.heappop(self._queue)

            # Initiate the call
            await self._handler.dial(qm.msg)

        # Reset processing flag and sleep task.
        self._task = None

        # If there are items in queue, schedule the next sleep.
        if self._queue:
            self._reschedule(self._queue[0].ts)

    def _reschedule(self, new_ts: float) -> None:
        """Schedule a task to sleep until the next item should be processed."""

        # If another sleep-and-process task is active, cancel it.
        # This situation only comes up if the task is in its sleeping phase.
        # The task will be cancelled and a new task will be scheduled.
        if self._task:
            self._task.cancel()

        # Schedule a task to sleep until it's time to process the next item.
        self._task = asyncio.ensure_future(
            self._sleep_and_process(new_ts), loop=self._loop
        )

    def put(self, item: Any, ts: float) -> None:
        """Add a new item to the queue."""

        # If the queue is empty, or if the new item precedes all items on the queue, adjust the
        # schedule accordingly.
        if not self._queue or self._queue[0].ts > ts:
            self._reschedule(ts)

        # Add item to queue.
        heapq.heappush(self._queue, QueuedMessage(ts, item))
