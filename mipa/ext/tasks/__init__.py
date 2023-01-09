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
from typing import Any, Callable, Coroutine, Dict, Optional

from mipa.exception import TaskNotRunningError

__all__ = ['Loop', 'loop']


class Loop:
    def __init__(
        self,
        func: Callable[..., Coroutine[Any, Any, Any]],
        seconds: int = 60,
        custom_loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        self.seconds: int = seconds
        self.func: Callable[..., Coroutine[Any, Any, Any]] = func
        self._task: Optional[asyncio.Task[Any]] = None
        self.stop_next_iteration = None
        self._loop: Optional[asyncio.AbstractEventLoop] = custom_loop

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
        _loop = (
            asyncio.get_running_loop() if self._loop is None else self._loop
        )  # self._loop が無いなら取得
        self._task = _loop.create_task(self.task(*args, **kwargs))
        return self._task

    def stop(self):
        """
        タスクを停止
        """

        if self._task is None:
            raise TaskNotRunningError('タスクは起動していません')

        if not self._task.done():
            self.stop_next_iteration = True

    async def task(self, *args: tuple[Any], **kwargs: Dict[Any, Any]):
        while True:
            if self.stop_next_iteration:
                return
            await self.func(self.seconds, *args, **kwargs)
            await asyncio.sleep(self.seconds)


def loop(n: int, custom_loop: Optional[asyncio.AbstractEventLoop] = None):
    def _deco(f: Callable[..., Coroutine[Any, Any, Any]]) -> Loop:
        return Loop(f, n, custom_loop=custom_loop)

    return _deco
