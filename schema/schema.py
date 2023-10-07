def individual_serial(profDetail) -> dict:
    return {
        "id": str(profDetail["_id"]),
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


