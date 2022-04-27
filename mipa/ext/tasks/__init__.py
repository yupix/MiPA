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
