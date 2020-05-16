import json
import datetime

from decimal import Decimal
from uuid import UUID


class Serializer:

    @staticmethod
    def dumps(obj, indent=4):
        """Converts List to Json String"""
        if isinstance(obj, list):
            return json.dumps(obj, default=lambda x: x.__dict__, cls=Serializer.CustomEncoder, sort_keys=True, indent=indent)

        """Converts to Json String"""
        if isinstance(obj, dict):
            return json.dumps(obj, cls=Serializer.CustomEncoder, sort_keys=True, indent=indent)

        return json.dumps(obj.__dict__, cls=Serializer.CustomEncoder, sort_keys=True, indent=indent).encode()

    @staticmethod
    def loads(obj):
        return json.loads(obj)

    @staticmethod
    def deserialize(obj, indent=4):
        return Serializer.loads(Serializer.dumps(obj, indent))

    class CustomEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return float("{:.2f}".format(obj))

            if isinstance(obj, UUID):
                return str(obj)

            if isinstance(obj, datetime.datetime):
                return obj.isoformat()

            return json.JSONEncoder.default(self, obj)


class JsonSerializable(object):
    def to_json(self, indent=4):
        return Serializer.deserialize(self, indent)
