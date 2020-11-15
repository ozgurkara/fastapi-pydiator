import json
import datetime

from decimal import Decimal
from uuid import UUID
from pydiator_core.serializer import BaseSerializer


class CustomSerializer(BaseSerializer):

    def dumps(self, obj, indent=4):
        """Converts List to Json String"""
        if isinstance(obj, list):
            return json.dumps(obj, default=lambda x: x.__dict__, cls=self.CustomEncoder, sort_keys=True,
                              indent=indent)

        """Converts to Json String"""
        if isinstance(obj, dict):
            return json.dumps(obj, cls=self.CustomEncoder, sort_keys=True, indent=indent)

        print("custom serializer")

        return json.dumps(obj.__dict__, cls=self.CustomEncoder, sort_keys=True, indent=indent).encode()

    def loads(self, obj):
        return json.loads(obj)

    def deserialize(self, obj, indent=4):
        return self.loads(self.dumps(obj, indent))

    class CustomEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return float("{:.2f}".format(obj))

            if isinstance(obj, UUID):
                return str(obj)

            if isinstance(obj, datetime.datetime):
                return obj.isoformat()

            return json.JSONEncoder.default(self, obj)
