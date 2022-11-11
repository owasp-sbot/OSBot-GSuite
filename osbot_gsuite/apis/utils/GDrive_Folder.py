from osbot_gsuite.apis.GDrive import GDrive
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.utils.Files import Files


class GDrive_Folder:

    def __init__(self, folder_name=None, folder_id=None):
        self.folder_name = folder_name
        self.folder_id   = folder_id
        self.gdrive = GDrive()

    def resolve_folder_id(self):
        if self.folder_id is None:
            mime_type = 'application/vnd.google-apps.folder'
            result = self.gdrive.find_by_name(self.folder_name, mime_type)
            if result:
                self.folder_id = result.get('id')
        return self

    def file_info(self, file_id):
        return self.gdrive.file_metadata(file_id=file_id, fields='*')

    def file_delete(self,file_id):
        return self.gdrive.file_delete(file_id)

    def file_upload(self, path, mime_type):
        print(f'uploading file: {path}')
        self.resolve_folder_id()
        if self.folder_id:
            return self.gdrive.file_upload(local_file=path, mime_type=mime_type, folder_id=self.folder_id)

    def file_upload_png(self, path):
        png_mime_type = 'image/png'
        return self.file_upload(path=path, mime_type=png_mime_type)

    @index_by
    def files(self, size=100, fields="files(id,name)"):
        return self.gdrive.files_in_folder(folder_id=self.folder_id, size=size, fields=fields)

        #file_id = self.graph_id_in_gdrive(file_name)

        #if file_id:  # if the file exists, delete it before uploading the new version
        #    Dev.pprint('deleting file: {0}'.format(file_id))
        #    self.gdrive.file_delete(file_id)

    def folder_create(self):
        self.resolve_folder_id()
        if self.folder_name and self.folder_id is None:
            return self.gdrive.folder_create(self.folder_name)