import json
from datetime import datetime
from typing import Any

from humps import camelize
from pydantic import BaseModel
from pydantic.generics import GenericModel

from emistream.time import stringify

DictType = dict[str, Any]


class SerializableModel(BaseModel):
    """Base class for models that can be serialized to JSON."""

    def json(self, *args, by_alias: bool = True, **kwargs) -> str:
        return super().json(*args, by_alias=by_alias, **kwargs)

    def dict(self, *args, by_alias: bool = True, **kwargs) -> DictType:
        return self.json_dict(*args, by_alias=by_alias, **kwargs)

    def json_dict(self, *args, **kwargs) -> DictType:
        return json.loads(self.json(*args, **kwargs))

    class Config:
        # Allow population by field name to allow for camelCase
        allow_population_by_field_name = True
        # Use camelCase for JSON keys
        alias_generator = camelize
        json_encoders = {
            # Use ISO 8601 for datetime
            datetime: stringify,
        }


class SerializableGenericModel(GenericModel):
    """Base class for generic models that can be serialized to JSON."""

    def json(self, *args, by_alias: bool = True, **kwargs) -> str:
        return super().json(*args, by_alias=by_alias, **kwargs)

    def dict(self, *args, by_alias: bool = True, **kwargs) -> DictType:
        return self.json_dict(*args, by_alias=by_alias, **kwargs)

    def json_dict(self, *args, **kwargs) -> DictType:
        return json.loads(self.json(*args, **kwargs))

    class Config:
        # Allow population by field name to allow for camelCase
        allow_population_by_field_name = True
        # Use camelCase for JSON keys
        alias_generator = camelize
        json_encoders = {
            # Use ISO 8601 for datetime
            datetime: stringify,
        }
