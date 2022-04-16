__all__ = ('RawActiveUsersChart', 'RawDriveRemoteChart', 'RawDriveLocalChart','RawDriveChart')

from typing import List

from mipac.types import ActiveUsersChartPayload, DriveChartPayload, DriveLocalChartPayload, DriveRemoteChartPayload


class RawActiveUsersChart:
    __slots__ = (
        'read_write',
        'read',
        'write',
        'registered_within_week',
        'registered_within_month',
        'registered_within_year',
        'registered_outside_week',
        'registered_outside_month',
        'registered_outside_year',
    )

    def __init__(self, data: ActiveUsersChartPayload):
        self.read_write: List[int] = data['read_write']
        self.read: List[int] = data['read']
        self.write: List[int] = data['write']
        self.registered_within_week: List[int] = data['registered_within_week']
        self.registered_within_month: List[int] = data['registered_within_month']
        self.registered_within_year: List[int] = data['registered_within_year']
        self.registered_outside_week: List[int] = data['registered_outside_week']
        self.registered_outside_month: List[int] = data['registered_outside_month']
        self.registered_outside_year: List[int] = data['registered_outside_year']


class RawDriveLocalChart:
    __slots__ = (
        'total_count',
        'total_size',
        'inc_count',
        'inc_size',
        'dec_count',
        'dec_size'
    )

    def __init__(self, data: DriveLocalChartPayload):
        self.total_count: List[int] = data['total_count']
        self.total_size: List[int] = data['total_size']
        self.inc_count: List[int] = data['inc_count']
        self.inc_size: List[int] = data['inc_size']
        self.dec_count: List[int] = data['dec_count']
        self.dec_size: List[int] = data['dec_size']


class RawDriveRemoteChart:
    __slots__ = (
        'total_count',
        'total_size',
        'inc_count',
        'inc_size',
        'dec_count',
        'dec_size'
    )

    def __init__(self, data: DriveRemoteChartPayload):
        self.total_count: List[int] = data['total_count']
        self.total_size: List[int] = data['total_size']
        self.inc_count: List[int] = data['inc_count']
        self.inc_size: List[int] = data['inc_size']
        self.dec_count: List[int] = data['dec_count']
        self.dec_size: List[int] = data['dec_size']


class RawDriveChart:
    __slots__ = ('local', 'remote')

    def __init__(self, data: DriveChartPayload):
        self.local: RawDriveLocalChart = RawDriveLocalChart(data['local'])
        self.remote: RawDriveRemoteChart = RawDriveRemoteChart(data['remote'])
