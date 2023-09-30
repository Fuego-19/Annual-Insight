def individual_serial(profDetail) -> dict:
    return {
        "id": str(profDetail["_id"]),
        "name": profDetail["name"],
        "phdYear": profDetail["phdYear"],
        "dateOfJoining": profDetail["dateOfJoining"],
        "primaryDept": profDetail["primaryDept"],
        "BroadRsrchDomain": profDetail["BroadRsrchDomain"]
    
    }

def list_serial(profDetails) -> list:
    return [individual_serial(profDetail)for profDetail in profDetails]

def research_contributions_serial(researchContribution) -> dict:
    return {
        "startDate": researchContribution["startDate"],
        "endDate": researchContribution["endDate"],
        "coAuthors": researchContribution["coAuthors"],
        "title": researchContribution["title"],
        "DOI": researchContribution["DOI"]
    }

def research_contributions_list_serial(researchContributions) -> list:
    return [research_contributions_serial(rc) for rc in researchContributions]

