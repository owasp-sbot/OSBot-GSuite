from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

from osbot_utils.utils.Objects import dict_to_obj

from osbot_utils.utils.Dev import pprint

from osbot_utils.decorators.methods.cache_on_self import cache_on_self

from osbot_gsuite.gsuite.GSuite import GSuite
from osbot_gsuite.gsuite.drive.GDrive import GDrive
from osbot_utils.base_classes.Type_Safe import Type_Safe


class GDocs(Type_Safe):
    gsuite : GSuite
    gdrive : GDrive

    # def __init__(self, gsuite_secret_id=None):
    #     self.docs   = GSuite(gsuite_secret_id).docs_v1().documents()
    #     self.gdrive = GDrive(gsuite_secret_id)

    @cache_on_self
    def docs_v1(self) -> Resource:
        return self.gsuite.docs_v1()

    @cache_on_self
    def documents(self) -> Resource:
        return self.docs_v1().documents()


    # methods
    def document_create(self, title, folder_id=None):
        body     = { 'title': title }
        doc_info = self.documents().create(body=body).execute()
        doc_id   = doc_info.get('documentId')
        if folder_id:
            self.gdrive.file_move_to_folder(doc_id, folder_id)

        return dict_to_obj(dict(doc_info  = doc_info ,
                                doc_id    = doc_id   ,
                                folder_id = folder_id))

    def document_delete(self, doc_id):
        return self.gdrive.file_delete(doc_id)

    def document_exists(self, doc_id):
        return self.document_info(doc_id) is not None

    def document_info(self, doc_id):
        try:
            doc_info = self.documents().get(documentId=doc_id).execute()
            return dict_to_obj(doc_info)
        except HttpError as http_error:
            if http_error.status_code != 404:
                raise http_error


    def execute_requests(self, file_id, requests):
        body = {'requests': requests}
        return self.documents().batchUpdate(documentId= file_id, body=body).execute()
