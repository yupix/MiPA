from typing import List, Optional

from mipac.core.models.drive import RawFile
from mipac.http import Route

# __all__ = ('MiFile', 'check_upload', 'get_file_ids')


class MiFile:
    __slots__ = (
        'path',
        'file_id',
        'name',
        'folder_id',
        'comment',
        'is_sensitive',
        'force',
    )

    def __init__(
        self,
        path: Optional[str] = None,
        file_id: Optional[str] = None,
        name: Optional[str] = None,
        folder_id: Optional[str] = None,
        comment: Optional[str] = None,
        is_sensitive: bool = False,
        force: bool = False,
    ):
        """
        Parameters
        ----------
        path : Optional[str], default=None
            path to a local file
        file_id : Optional[str], default=None
            ID of the file that exists on the drive
        name Optional[str], default=None
            file name
        folder_id : Optional[str], default=None
            Folder ID
        comment : Optional[str], default=None
            Comments on files
        is_sensitive : Optional[str], default=None
            Whether this item is sensitive
        force : bool, default=False
            Whether to force overwriting even if it already exists on the drive
        """
        self.path = path
        self.file_id = file_id
        self.name = name
        self.folder_id = folder_id
        self.comment = comment
        self.is_sensitive = is_sensitive
        self.force = force


# async def check_upload(files: List[MiFile]):
#     _files = []
#     for file in files:
#         if file.path:
#             endpoint = Route('POST', '/api/drive/files/create')
#             data = {'file': open(file.path, 'rb'),
#                     'name': file.name,
#                     'folderId': file.folder_id,
#                     'isSensitive': file.is_sensitive,
#                     'comment': file.comment,
#                     'force': file.force}
#             _files.append(RawFile(await HTTPSession.request(endpoint, auth=True, data=data, lower=True)).id)  # TODO: 治す
#         else:
#             _files.append(file.file_id)
#
#     return _files


# async def get_file_ids(files: List[MiFile]):
#     return await check_upload(files)
