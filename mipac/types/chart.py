__all__ = ('ActiveUsersChartPayload', 'DriveLocalChartPayload', 'DriveRemoteChartPayload', 'DriveChartPayload')

from typing import List, TypedDict, Union


class ActiveUsersChartPayload(TypedDict):
    read_write: List[int]
    read: List[int]
    write: List[int]
    registered_within_week: List[Union[int]]
    registered_within_month: List[int]
    registered_within_year: List[int]
    registered_outside_week: List[int]
    registered_outside_month: List[int]
    registered_outside_year: List[int]


class DriveLocalChartPayload(TypedDict):
    total_count: List[int]
    total_size: List[int]
    inc_count: List[int]
    inc_size: List[int]
    dec_count: List[int]
    dec_size: List[int]


class DriveRemoteChartPayload(TypedDict):
    total_count: List[int]
    total_size: List[int]
    inc_count: List[int]
    inc_size: List[int]
    dec_count: List[int]
    dec_size: List[int]


class DriveChartPayload(TypedDict):
    local: DriveLocalChartPayload
    remote: DriveRemoteChartPayload
