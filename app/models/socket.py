from pydantic import BaseModel


## Used for Login & shared by all
class WSIncomming(BaseModel):
    action: str
    payload: dict
