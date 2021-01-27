from dropbox.files import FolderMetadata

from .dropbox import DropBoxStorage

def human_readable(size):
    if size < 1024:
        return size
    seq = ['', ' KB', ' MB', ' GB', ' TB']
    exp = 0
    while size > 1023:
        size = size / 1024.0
        exp += 1
    label = f"{size:.3f}"[:4]
    if label[-1] == '.':
        label = label[:-1]
    return label + seq[exp]


class DropboxMetaFile:

    def __init__(self, metadata):
        self.path = metadata.path_display
        self.url = self.path[1:]
        self.name = metadata.name
        if isinstance(metadata, FolderMetadata):
            self.is_dir = True
        else:
            self.is_dir = False
            self.date = metadata.server_modified
            self.size = human_readable(metadata.size)


class DropboxWrapper():

    def __init__(self, keys_filename):
        self.storage = None
        self.keys_filename = keys_filename
        self._attempt_access()

    def _attempt_access(self):
        try:
            with open(self.keys_filename) as filedata:
                token = filedata.readlines()[1].strip()
            self.storage = DropBoxStorage(oauth2_access_token=token)
            self.storage.client.users_get_current_account()
        except Exception as e:
            print(e)
            self.storage = None

    def has_access(self):
        if not self.storage:
            self._attempt_access()
        return self.storage

    def listdir(self, path):
        # return self.storage.listdir(path)
        result = self.storage.client.files_list_folder(path)
        files = list()
        for metadata in result.entries:
            files.append(DropboxMetaFile(metadata))
        files.sort(key=lambda fi: fi.name.lower())
        files.sort(key=lambda fi: -1 if fi.is_dir else 1)
        return files

    def get_file(self, name):
        return self.storage.open(name)

