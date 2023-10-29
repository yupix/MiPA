"""
The MIT License (MIT)

Copyright (c) 2015-present Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

The Software is modified as follows:
    - Delete unused functions and method.
    - Removing functions beyond what is necessary to make it work.
    - Simplification of some functions.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import asyncio
import inspect
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    Generic,
    Optional,
    Type,
    TypeVar,
)

from mipa.exception import TaskNotRunningError
from mipa.utils import MISSING

__all__ = ["Loop", "loop"]

_func = Callable[..., Coroutine[Any, Any, Any]]
LF = TypeVar("LF", bound=_func)
T = TypeVar("T")


class Loop(Generic[LF]):
    def __init__(
        self,
        coro: LF,
        seconds: float,
        count: Optional[int],
    ):
        self.seconds = seconds
        self.coro: LF = coro
        self.count: Optional[int] = count
        self._current_loop = 0
        self._task: Optional[asyncio.Task[None]] = None
        self._injected = None

        self._stop_next_iteration = False

        if self.count is not None and self.count <= 0:
            raise ValueError("count must be greater than 0 or None.")

        if not inspect.iscoroutinefunction(self.coro):
            raise TypeError(
                f"Expected coroutine function, not {type(self.coro).__name__!r}."
            )

    def start(
        self, *args: tuple[Any], **kwargs: Dict[Any, Any]
    ) -> asyncio.Task[Any]:
        """
        タスクを開始する

        Parameters
        ----------
        args : Any
        kwargs : Any

        Returns
        -------
        _task : asyncio.Task[Any]
        """
        if self._injected is not None:
            args = (self._injected, *args)
        self._task = asyncio.create_task(self._loop(*args, **kwargs))
        return self._task

    def stop(self):
        """
        タスクを停止
        """

        if self._task is None:
            raise TaskNotRunningError("タスクは起動していません")

        if not self._task.done():
            self._stop_next_iteration = True

    async def _loop(self, *args: tuple[Any], **kwargs: Dict[Any, Any]):
        while True:
            if self._stop_next_iteration is True:
                return
            await self.coro(*args, **kwargs)
            await asyncio.sleep(self.seconds)

            self._current_loop += 1
            if self._current_loop == self.count:
                break

    def __get__(self, obj: T, objtype: Type[T]):
        if obj is None:
            return self

        copy: Loop[LF] = Loop(
            self.coro,
            seconds=self.seconds,
            count=self.count,
        )
        copy._injected = obj

        setattr(obj, self.coro.__name__, copy)
        return copy


def loop(
    *,
    seconds: float = MISSING,
    count: Optional[int] = None,
) -> Callable[[LF], Loop[LF]]:
    def decorator(func: LF) -> Loop[LF]:
        return Loop[LF](
            func,
            seconds=seconds,
            count=count,
        )

    return decorator
