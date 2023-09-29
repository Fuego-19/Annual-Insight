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