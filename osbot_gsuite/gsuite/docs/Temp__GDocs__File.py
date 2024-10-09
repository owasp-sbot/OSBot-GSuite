from types                                          import SimpleNamespace
from osbot_gsuite.gsuite.docs.GDocs                 import GDocs
from osbot_utils.utils.Misc                         import random_text
from osbot_gsuite.testing.OSBot__GSuite__Testing    import osbot_gsuite_testing
from osbot_utils.base_classes.Type_Safe             import Type_Safe


class Temp__GDocs__File(Type_Safe):
    gdocs    : GDocs
    title    : str = random_text('osbot-gsuite-random-file')
    doc_data : SimpleNamespace
    doc_id   : str

    def parent_folder(self):
        return osbot_gsuite_testing.gdrive_temp_folder()

    def __enter__(self):
        self.file_create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_delete()

    def file_create(self):
        kwargs = dict(title   = self.title    ,
                      folder_id = self.parent_folder())
        self.doc_data = self.gdocs.document_create(**kwargs)
        self.doc_id   = self.doc_data.doc_id
        return self.doc_id

    def file_delete(self):
        return self.gdocs.document_delete(self.doc_id)

    def file_exists(self):
        return self.gdocs.document_exists(self.doc_id)

    def file_info(self):
        return self.gdocs.document_info(self.doc_id)