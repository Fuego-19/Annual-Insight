from pydantic import BaseModel
from datetime import datetime


class profDetail(BaseModel):
    profId: str
    name: str
    email: str
    phdYear: str
    dateOfJoining: datetime
    primaryDept: str
    BroadRsrchDomain: list

class coAuthor(BaseModel):
    name: str
    role: str

class author():
    authorId : str
    papers_list: list
    authorName: str
    designation: str

class paperAuthor():
    authorId:str
    papers: list
    authorName: str
    designation: str
class researchPaper():
    paperId: str
    authors: list
    title: str
    pages: str
    volume: str
    number: str
    issue: str
    date: str
    publisher: str
    doi: str
    articleno: str
    
class researchContributions(BaseModel):
    dateOfPublication: datetime
    publisherEmail: str
    isPublished: bool
    coAuthors: list[dict]
    title: str
    DOI: str


    