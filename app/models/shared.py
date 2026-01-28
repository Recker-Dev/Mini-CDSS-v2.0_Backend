from typing import Annotated, Any
from bson import ObjectId
from pydantic import (
    PlainSerializer,
    BeforeValidator,
)


#### Custom Data Type to Handle conversion between Mongo-ObjectId and str on JSON end####
def convert_obj_to_str(v: Any) -> str:
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, str):
        return v
    raise ValueError("Failed Serialization; Invalid datatype of Id field; neither str nor ObjectId")

def convert_str_to_obj(v: Any) -> ObjectId:
    if isinstance(v, str):
        return ObjectId(v)
    if isinstance(v, ObjectId):
        return  v
    raise ValueError("Faled Validation; Invalid datatype of Id field; neither str nor ObjectId")

## Creates a custom datatype with its own Serialization Logic
MongoDbId = Annotated[
    Any,  ## Its jst written as Any but is ObjectId or str; using Union it crashed
    BeforeValidator(convert_str_to_obj),
    PlainSerializer(lambda x: convert_obj_to_str(x), return_type=str, when_used="json"),
]
