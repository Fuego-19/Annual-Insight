def individual_serial(profDetail) -> dict:
    return {
        "id": str(profDetail["_id"]),
        "profId": str(profDetail["profId"]),
        "email": str(profDetail["email"]),
        "name": profDetail["name"],
        "phdYear": profDetail["phdYear"],
        "dateOfJoining": profDetail["dateOfJoining"],
        "primaryDept": profDetail["primaryDept"],
        "BroadRsrchDomain": profDetail["BroadRsrchDomain"]
    
    }

def list_serial(profDetails) -> list:
    return [individual_serial(profDetail)for profDetail in profDetails]



def co_author_serial(coAuthor: dict) -> dict:
    return {
        "name": coAuthor["name"],
        "role": coAuthor["role"]
    }
def research_contributions_serial(researchContribution) -> dict:
    co_authors = []
    print("gg")
    print(researchContribution["coAuthors"])
    print(type(researchContribution["coAuthors"]))
    for coAuthor in researchContribution["coAuthors"]:
        co_authors.append(dict(coAuthor))

    return {
        "publisherEmail": researchContribution["publisherEmail"],
        "isPublished": researchContribution["isPublished"],
        "dateOfPublication": researchContribution["dateOfPublication"],
        "coAuthors": co_authors,
        "title": researchContribution["title"],
        "DOI": researchContribution["DOI"]
    }

def research_contributions_list_serial(researchContributions) -> list:
    return [research_contributions_serial(rc) for rc in researchContributions]


def author_serial(author_data) -> dict:
    return {
        "authorId": str(author_data.authorId),
        "papers": author_data.papers,
        "authorName": author_data.authorName,
        "designation": author_data.designation
    }
def author_list_serial(authors) -> list:
    return [author_serial(auth) for auth in authors]


def research_paper_serial(paper_data) -> dict:
    return {
        "paperId": str(paper_data.paperId),
        "authors": paper_data.authors,
        "title": paper_data.title,
        "pages": paper_data.pages,
        "volume": paper_data.volume,
        "number": paper_data.number,
        "issue": paper_data.issue,
        "date": paper_data.date,
        "publisher": paper_data.publisher,
        "doi": paper_data.doi,
        "articleno": paper_data.articleno
    }
    
def research_paper_list_serial(papers) -> list:
    return [research_paper_serial(paper) for paper in papers]
