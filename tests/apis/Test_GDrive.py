from unittest        import TestCase

from osbot_gsuite.apis.GDrive import GDrive
from osbot_utils.utils.Dev import Dev

class Test_GDrive(TestCase):
    def setUp(self):
        self.gdrive = GDrive()

    def test_ctor(self):
        files = self.gdrive.files
        assert files._baseUrl == 'https://www.googleapis.com/drive/v3/'

    def test_file_find_by_name(self):
        name   = 'GSlides API tests'
        assert self.gdrive.find_by_name(name).get('name') == name
        assert self.gdrive.find_by_name('aaaa') is None

    def test_file_export(self):
        #id = '1rWCUAh2y4AY-RrqyK5JywDskGjJe4GydrPSrX1td6Lk'   # test document
        #id = '1CA-uqZj9HVr2_RHiI-esVyHBoHZ1M1sxGzq54EQ2Ek4'   # test slides
        file_id = self.gdrive.find_by_name('GSlides API tests').get('id')
        pdf_data = self.gdrive.file_export(file_id)

        with open('./test.pdf', "wb") as fh:
            fh.write(pdf_data)
            #fh.write(base64.decodebytes(pdf_data.encode()))
        #Dev.pprint(result)

    def test_file_metadata(self):
        file_id = '1rWCUAh2y4AY-RrqyK5JywDskGjJe4GydrPSrX1td6Lk'            # test document
        result  = self.gdrive.file_metadata(file_id)
        Dev.pprint(result)

    def test_file_metadata_update(self):
        file_id = '1CA-uqZj9HVr2_RHiI-esVyHBoHZ1M1sxGzq54EQ2Ek4'            # test spreadsheet
        metadata = self.gdrive.file_metadata(file_id)
        Dev.pprint(metadata)
        changes =  self.gdrive.set_file_title(file_id,'GSlides API tests')
        Dev.pprint(changes)

    # def test_file_update(self):
    #     file   = '/tmp/puml_graph_W64.png'
    #     #file   = '/tmp/puml_graph_09Q.png'
    #     file   = '/tmp/puml_graph.png'
    #     id     = '1H72nAFgqu1OSW_xm-gwDWml6tOzy5UZ_'
    #     result = self.gdrive.file_update(file,'image/png',id)
    #     Dev.pprint(result)

    def test_file_share_with_domain(self):
        file_id = '1BvhH00qomATK6YFB3afQwe2GJeS_VLdikhuPdAE0ev0'
        result = self.gdrive.file_share_with_domain(file_id, 'owasp.org')
        Dev.pprint(result)

    def test_file_upload(self):
        #file   = '/tmp/puml_graph_W64.png'
        file   = '/tmp/puml_graph_09Q.png'
        folder = '1ZXXoYc443-HG6Twr7chTvym8JNgssoNJ'
        result = self.gdrive.file_upload(file,'image/png',folder)
        Dev.pprint(result)

    def test_files(self):
        files = self.gdrive.files_all(4)
        for item in files:
            print('{0:22} - {1}'.format(item['name'], item['id']))

    def test_files_in_folder(self):
        folder_id = '16yOkKyi0TfOy3w4IMW40vo-pr--Wa1Y9'
        try:
            files = self.gdrive.files_in_folder(folder_id,size=2)
            for item in files:
                print('{0:22} - {1}'.format(item['name'], item['id']))
        except Exception as error:
            Dev.pprint(error)


    def testfiles_with_mime_type(self):
        mime_type_presentations = 'application/vnd.google-apps.presentation'
        files = self.gdrive.find_by_mime_type(mime_type_presentations)

        assert len(files) > 0



    def test_drive_activity(self):
        import google.auth
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        # Authenticate and authorize the credentials
        creds, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/drive.activity'])
        drive_activity = build('driveactivity', 'v2', credentials=creds)

        # Define the parameters for the API request
        request_params = {
            'pageSize': 10,  # Max number of activity events to return
            'filter': "time >= '2022-01-01T00:00:00.000Z'",  # Filter by date range
            'orderBy': 'time desc'  # Sort by most recent events first
        }

        # Call the API to get the activity events
        response = drive_activity.activity().query(**request_params).execute()
