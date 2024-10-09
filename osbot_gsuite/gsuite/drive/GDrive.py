from googleapiclient.discovery import Resource
from googleapiclient.http    import MediaFileUpload
from osbot_utils.base_classes.Type_Safe import Type_Safe

from osbot_gsuite.gsuite.GSuite                     import GSuite
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.utils.Dev                          import Dev
from osbot_utils.utils.Files                        import Files


class GDrive(Type_Safe):
    gsuite: GSuite

    @cache_on_self
    def drive_v3(self) -> Resource:                                       # todo refactor into drive_v3
        return self.gsuite.drive_v3()

    @cache_on_self
    def files(self):
        return self.drive_v3().files()

    @cache_on_self
    def permissions(self):
        return self.drive_v3().permissions()

    def execute(self, command):
        try:
            return command.execute()
        except Exception as error:
            Dev.pprint(error)                   # add better error handling log capture
            return None

    def folder_create(self, folder_name):
        return self.file_create(file_type='application/vnd.google-apps.folder', title=folder_name)

    def file_create(self, file_type, title, folder=None):
        file_metadata = {
            "mimeType": file_type,
            "name": title
        }
        if folder:
            file_metadata["parents"] =  [folder]
        file = self.files().create(body=file_metadata, fields='id').execute()
        return file.get('id')

    def file_export(self, file_Id):
        return self.files().export(fileId=file_Id, mimeType='application/pdf').execute()

    def file_export_as_pdf_to(self,file_id,target_file):
        pdf_data = self.file_export(file_id)
        with open(target_file, "wb") as fh:
            fh.write(pdf_data)
        return target_file

    def file_metadata(self, file_id, fields = "id,name"):
        return self.execute(self.files().get(fileId = file_id, fields=fields))

    def file_metadata_update(self, file_id, changes):
        return self.files().update(fileId=file_id, body=changes).execute()

    def file_delete(self, file_id):
        if file_id:
            self.files().delete(fileId= file_id).execute()

    def file_share_with_domain(self,file_id,domain):
        domain_permission = {
            'type': 'domain',
            'role': 'writer',
            'domain': domain,
        }
        return self.permissions().create(fileId=file_id, body=domain_permission, fields='id').execute()

    def file_update(self, file_id, body):
        return self.files().update(fileId=file_id, body=body).execute()
        # if Files.exists(local_file):
        #     file_metadata = {'name': Files.file_name(local_file)}
        #     media = MediaFileUpload(local_file, mimetype=mime_type)
        #     file = self.files().update(body=file_metadata, media_body=media, fileId= file_id, fields='id').execute()
        #     return file.get('id')
        #return None

    def file_upload(self, local_file, mime_type, folder_id=None):
        if Files.exists(local_file):
            file_metadata = {'name': Files.file_name(local_file), 'parents': [folder_id]}
            media = MediaFileUpload(local_file, mimetype=mime_type)
            file = self.files().create(body=file_metadata, media_body=media, fields='id').execute()
            return file.get('id')
        return None

    def file_weblink(self, file_id):
        return 'https://drive.google.com/open?id={0}'.format(file_id)

    def files_all(self, size, fields="files(id,name)"):
        results = self.files().list(pageSize=size, fields=fields).execute()
        return results.get('files', [])

    def files_in_folder(self, folder_id, size=100, fields="files(id,name)"):
        results = self.files().list(q="parents='{0}' and trashed = false".format(folder_id),pageSize=size, fields=fields).execute()
        return results.get('files', [])

    def find_by_name(self, name, mime_type = None):
        if mime_type:
            query = "name = '{0}' and mimeType = '{1}'".format(name,mime_type)
        else:
            query = "name = '{0}'".format(name)
        results = self.execute(self.files().list(q=query))  # , fields="files(id,name)"))
        if results and len(results.get('files')) > 0:
            return results.get('files').pop()
        return None

    def find_by_mime_type(self, mime_type):
        results = self.execute(self.files().list(q="mimeType = '{0}'".format(mime_type), fields="files(id,name)"))
        if results:
            return results.get('files', [])

    def set_file_title(self, file_id, new_title):
        return self.file_metadata_update(file_id, {"name" : new_title })
