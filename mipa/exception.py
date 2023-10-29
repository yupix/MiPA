__all__ = (
    "MIPABaseException",
    "MIPABaseWebSocketError",
    "WebSocketNotConnected",
    "WebSocketReconnect",
    "CogNameDuplicate",
    "ExtensionAlreadyLoaded",
    "ExtensionFailed",
    "InvalidCogPath",
    "NoEntryPointError",
    "ClientConnectorError",
    "TaskNotRunningError",
)


class MIPABaseException(Exception):
    """MIPA Base Exception"""


class MIPABaseWebSocketError(MIPABaseException):
    """Websocket Base Exception"""


class WebSocketNotConnected(MIPABaseWebSocketError):
    """Websocket not connected"""


class WebSocketReconnect(MIPABaseWebSocketError):
    """Websocket should reconnect"""


class CogNameDuplicate(MIPABaseException):
    """Cogの名前が重複している"""


class ExtensionNotLoaded(MIPABaseException):
    """Cogが読み込まれていない"""


class ExtensionAlreadyLoaded(MIPABaseException):
    """Cogは既に読み込まれている"""


class ExtensionFailed(MIPABaseException):
    """Cog周りのエラー"""


class InvalidCogPath(MIPABaseException):
    """無効なCogのパス"""


class NoEntryPointError(MIPABaseException):
    """Cogにsetup関数が存在しない"""


class ClientConnectorError(MIPABaseException):
    """WebSocketの接続に問題が発生した"""


class TaskNotRunningError(MIPABaseException):
    """タスクが動いてない状態で停止しようとした"""
