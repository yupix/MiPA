class NotExistRequiredData(Exception):
    """クラスの中に必要なデータが不足している"""


class ParameterError(Exception):
    """引数に関するエラー"""


class NotSupportedError(Exception):
    """特定のForkでサポートしていない場合のエラー"""


class APIError(Exception):
    """APIのエラー"""
