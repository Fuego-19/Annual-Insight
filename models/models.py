from pydantic import BaseModel
from datetime import datetime


class profDetail(BaseModel):
    
    name: str
    email: str
    phdYear: str
    dateOfJoining: datetime
    primaryDept: str
    BroadRsrchDomain: list

class coAuthor(BaseModel):
    name: str
    role: str
    
class researchContributions(BaseModel):
    dateOfPublication: datetime
    publisherEmail: str
    isPublished: bool
    coAuthors: list[dict]
    title: str
    DOI: str


    