from . import MongoModel
from flask import current_app as app


class Title(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('name', str, ''),
            ('comments', str, ''),
            ('publish_time', str, ''),
            ('detail', str, ''),
        ]
        fields.extend(super()._fields())
        return fields