from osbot_gsuite.apis.GDrive import GDrive
from osbot_gsuite.apis.GSuite import GSuite


class GDocs:

    def __init__(self, gsuite_secret_id=None):
        self.docs   = GSuite(gsuite_secret_id).docs_v1().documents()
        self.gdrive = GDrive(gsuite_secret_id)


    def execute_requests(self, file_id, requests):
        body = {'requests': requests}
        return self.docs.batchUpdate(documentId= file_id, body=body).execute()