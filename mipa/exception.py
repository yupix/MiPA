__all__ = (
    'WebSocketReconnect',
    'CogNameDuplicate',
    'ExtensionAlreadyLoaded',
    'ExtensionFailed',
    'InvalidCogPath',
    'NoEntryPointError',
    'ClientConnectorError',
    'TaskNotRunningError',
)


class WebSocketReconnect(Exception):
    """Websocketに再接続が必要"""


class CogNameDuplicate(Exception):
    """Cogの名前が重複している"""


class ExtensionAlreadyLoaded(Exception):
    """Cogは既に読み込まれている"""


class ExtensionFailed(Exception):
    """Cog周りのエラー"""


class InvalidCogPath(Exception):
    """無効なCogのパス"""


class NoEntryPointError(Exception):
    """Cogにsetup関数が存在しない"""


class ClientConnectorError(Exception):
    """WebSocketの接続に問題が発生した"""


class TaskNotRunningError(Exception):
    """タスクが動いてない状態で停止しようとした"""
