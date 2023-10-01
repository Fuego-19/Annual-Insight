from pydantic import BaseModel
from datetime import datetime

class profDetail(BaseModel):
    name: str
    phdYear: str
    dateOfJoining: datetime
    primaryDept: str
    BroadRsrchDomain: list

class researchContributions(BaseModel):
    startDate: datetime
    endDate: datetime
    coAuthors: list
    title: str
    DOI: str
