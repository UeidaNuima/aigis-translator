from mongoengine import *


class FileData(EmbeddedDocument):
    origin = StringField(required=True)
    translation = StringField()
    time_stamp = IntField(required=True)
    translator_name = StringField()
    translator_ip = StringField()
    index = IntField(required=True)


class File(Document):
    path = ListField()
    name = StringField(required=True)
    file_type = StringField(required=True, db_field='type')
    data = SortedListField(EmbeddedDocumentField(FileData), ordering='index')
    time_stamp = IntField(required=True)
    md5 = StringField(required=True)
