from pydantic import BaseModel
from datetime import datetime

class profDetail(BaseModel):
    name: str 
    phdYear: str
    dateOfJoining: datetime
    primaryDept: str
    BroadRsrchDomain: str
    