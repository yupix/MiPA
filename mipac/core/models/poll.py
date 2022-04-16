from typing import List, Optional


__all__ = ['RawPollChoices', 'RawPoll']

from mipac.types import PollPayload


class RawPollChoices:
    """
    Attributes
    ----------
    text : str
        アンケートの項目名
    votes : int
        投票数
    is_voted : bool
        投票済みか否か
    """

    __slots__ = ('text', 'votes', 'is_voted')

    def __init__(self, data):
        self.text: str = data["text"]
        self.votes: int = data["votes"]
        self.is_voted: bool = data["isVoted"]


class RawPoll:
    """
    Attributes
    ----------
    multiple : Optional[bool]
        複数回投票可能か否か
    expires_at : Optional[int]
        投票期限
    choices : Optional[List[RawPollChoices]]
        項目
    expired_after : Optional[int]
        残り期限
    """

    __slots__ = ('multiple', 'expires_at', 'choices', 'expired_after')

    def __init__(self, data: PollPayload):
        self.multiple: Optional[bool] = data.get("multiple")
        self.expires_at: Optional[int] = data.get("expires_at")
        self.choices: Optional[List[RawPollChoices]] = [RawPollChoices(i) for i in data['choices']] if data.get(
            "choices") else None
        self.expired_after: Optional[int] = data.get("expired_after")
