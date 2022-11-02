
from osbot_gsuite.apis.GDrive           import GDrive
from osbot_utils.utils.Dev import Dev
from osbot_utils.utils.Files import Files


class GSBot_to_GDrive:
    def __init__(self,gsuite_secret_id=None):
        self.target_folder  = 'gsbot-graphs'
        self.gdrive         = GDrive(gsuite_secret_id)

    def target_folder_id(self):
        mime_type = 'application/vnd.google-apps.folder'
        return self.gdrive.find_by_name(self.target_folder, mime_type).get('id')

    def graph_id_in_gdrive(self, file_name):
        file_metadata = self.gdrive.find_by_name(file_name)
        if file_metadata:
            return file_metadata.get('id')
        return None

    def upload_png_file_to_gdrive(self, png_file):
        #png_file  = GSBot_Helper().get_png_from_saved_graph(graph_name)
        file_name = Files.file_name(png_file)
        folder_id = self.target_folder_id()
        file_id   = self.graph_id_in_gdrive(file_name)

        if file_id:         # if the file exists, delete it before uploading the new version
            Dev.pprint('deleting file: {0}'.format(file_id))
            self.gdrive.file_delete(file_id)
        return self.gdrive.file_upload(png_file, 'image/png', folder_id)
        # can't use the code below because, the update wasn't working due to GSlides keeping (somewhere) a cache of the previous value
        #                                   update: (Oct 2022): GSlides will create a copy of the file uploaded to googleusercontent.com (which is what is then used in the GSlides)
        # if file_id is None:
        #     return self.gdrive.file_upload(png_file,'image/png', folder_id)
        # else:
        #     return self.gdrive.file_update(png_file, 'image/png', file_id )
