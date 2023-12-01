from fastapi import APIRouter
from models.models import profDetail, researchContributions,researchPaper,author,paperAuthor
from config.database import prof_collection, research_collection,authors_collection,papers_collection
from schema.schema import research_contributions_list_serial,list_serial,individual_serial,author_list_serial,research_paper_list_serial
from bson import ObjectId
from fastapi import HTTPException
import requests
from reportlab.platypus import Image
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fastapi.responses import FileResponse  
from reportlab.lib.colors import cyan
from datetime import date
import textwrap
from typing import Optional
import json
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from models.models import researchContributions
from bson import ObjectId
from pydantic import BaseModel
import random
import string

router = APIRouter()


@router.get("/papersByAuthorName")
async def get_papers_by_author_name(author_name: str = Query(..., title="Author Name")):
    try:
        # Find the author by their name
        author = authors_collection.find_one({"authorName": author_name})

        if author:
            # Retrieve the list of paper IDs associated with the author
            paper_ids = author.get("papers", [])
            print("gg5", paper_ids)
            # Query the papers_collection using the list of paper IDs
            papers = research_paper_list_serial(
                papers_collection.find({
                    "paperId": {"$in": paper_ids}
                })
            )

            return papers
        else:
            return []  # Return an empty list if the author is not found
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/papersByAuthorCount")
async def get_papers_by_author_count(min_author_count: int = Query(..., title="Minimum Author Count")):
    try:
        # Retrieve all papers from the collection
        all_papers = papers_collection.find()
        
        # Filter papers based on the number of authors exceeding the specified count
        filtered_papers = [paper for paper in all_papers if len(paper.get("authors", [])) > min_author_count]
        
        if not filtered_papers:
            raise HTTPException(status_code=404, detail=f"No papers found with more than {min_author_count} authors")
        
        # Serialize the filtered papers
        papers = research_paper_list_serial(filtered_papers)
        return papers
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/authorsByPaperCount")
async def get_authors_by_paper_count(min_paper_count: int = Query(..., title="Minimum Paper Count")):
    try:
        # Retrieve all authors from the collection
        all_authors = authors_collection.find()
        
        # Filter authors based on the number of papers exceeding the specified count
        filtered_authors = [auth for auth in all_authors if len(auth.get("papers", [])) >= min_paper_count]
        
        if not filtered_authors:
            raise HTTPException(status_code=404, detail=f"No authors found with more than {min_paper_count} papers")
        
        # Serialize the filtered authors
        authors = author_list_serial(filtered_authors)
        return authors
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/authorsByPartialPaperName")
async def get_authors_by_partial_paper_name(paper_name: str = Query(..., title="Partial Paper Name")):
    try:
        # Construct a regex pattern to match the partial paper name
        regex_pattern = {"$regex": paper_name, "$options": "i"}  # "i" makes the search case-insensitive

        # Query the papers_collection for papers that match the partial name
        papers = papers_collection.find({"title": regex_pattern})

        matched_papers = [paper for paper in papers]

        if matched_papers:
            # Retrieve all unique author IDs associated with the matched papers
            author_ids = list(set(author_id for paper in matched_papers for author_id in paper.get("authors", [])))
            print("Author IDs associated with the matched papers:", author_ids)
            
            # Query the authors_collection using the list of unique author IDs
            authors = author_list_serial(
                authors_collection.find({
                    "authorId": {"$in": author_ids}
                })
            )

            return authors
        else:
            return []  # Return an empty list if no matching papers are found
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/papersByAuthorDesignation")
async def get_papers_by_author_designation(designation: str = Query(..., title="Author Designation")):
    try:
        # Find authors with the specified designation
        authors_with_designation = authors_collection.find({"designation": designation})

        if authors_with_designation:
            # Extract author IDs of authors with the specified designation
            author_ids_with_designation = [author["authorId"] for author in authors_with_designation]
            print("Author IDs with the given designation:", author_ids_with_designation)

            # Query papers_collection to retrieve papers of authors with the specified designation
            papers = research_paper_list_serial(
                papers_collection.find({
                    "authors": {"$in": author_ids_with_designation}
                })
            )

            return papers
        else:
            return []  # Return an empty list if no authors with the specified designation are found
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

def generate_user_id(length=6):
    characters = string.ascii_letters + string.digits  # Combining letters and digits
    user_id = ''.join(random.choice(characters) for _ in range(length))
    return user_id






    
teal_color = (63/255, 173/255, 168/255)

@router.get("/")
async def get_profDetails():
    try:
        ProfDetails = list_serial(prof_collection.find())
        return ProfDetails
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/addProfile")
async def add_profDetails(profDetail: profDetail):
    print(profDetail)
    temp_dict = dict(profDetail)
    temp_dict["profId"] = generate_user_id(8)
    prof_collection.insert_one(temp_dict)

@router.post("/addResearchContributions")
async def add_researchContributions(researchContributions: researchContributions):
    print("hi")
    print(researchContributions)
    research_collection.insert_one(dict(researchContributions))

@router.get("/getAllContributions")
async def get_all_contributions():
    try:
        researchDetails = research_contributions_list_serial(research_collection.find())
        return researchDetails
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/getAllAuthors")
async def get_all_authors():
    try:
        authorDetails = author_list_serial(authors_collection.find())
        return authorDetails
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/getAllPapers")
async def getAllPapers():
    try:
        paperDetails = research_paper_list_serial(papers_collection.find())
        return paperDetails
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/generatePDF")
async def generate_pdf_endpoint(data: dict):
    try:
        prof_detail_data = list_serial(prof_collection.find())
        print("prof", prof_detail_data)
        research_contributions_data = research_contributions_list_serial(research_collection.find())
        pdf_filename = f"{prof_detail_data[0]['name']}_report.pdf"

        generate_pdf(prof_detail_data, research_contributions_data, pdf_filename)

        return FileResponse(pdf_filename, headers={"Content-Disposition": f"attachment; filename={pdf_filename}"})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))






def get_current_academic_year():
    today = date.today()
    current_year = today.year
    if today.month < 8:  # Academic year starts in August
        start_year = current_year - 1
    else:
        start_year = current_year
    end_year = start_year + 1

    academic_year_string = f"Academic Year: {start_year}-{end_year}"
    return academic_year_string

def changeFontToCyan(c):
      # RGB values for #3FADA8
    c.setFillColorRGB(*teal_color)
    c.setFont("Helvetica-Bold", 14)
    

    
def changeFontToBlack(c):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 10)





    
# @router.post("/testing")
# async def test2(requestData):
#     try:
#         print('dkfjdskf')
#         print(requestData)

#         text= {"text": "hello ji"}
#         return json.dumps(text)
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail=str(e))
    
class MyDataModel(BaseModel):
    key1: str

def extract_authors(input_string):
    authors = []
    author_list = input_string.split(" and ")

    for author in author_list:
        # Split each author into first and last name
        names = author.split(", ")
        if len(names) == 2:
            last_name, first_name = names
            authors.append(f"{first_name.capitalize()} {last_name.capitalize()}")

    return authors

def format_date(input_dict):
    month_dict = {
        'January': '01',
        'February': '02',
        'March': '03',
        'April': '04',
        'May': '05',
        'June': '06',
        'July': '07',
        'August': '08',
        'September': '09',
        'October': '10',
        'November': '11',
        'December': '12'
    }

    year = input_dict.get("year", None)
    month = input_dict.get("month", None)
    day = input_dict.get("day", None)

    if year is None:
        return None  # Year is required, so if it's missing, return None

    if day is not None and month is not None:
        month_numeric = month_dict.get(month, None)
        if month_numeric:
            date_string = f"{day}/{month_numeric}/{year}"
            return date_string
    else:
        return year  # If day is missing, return only the year
def parseAcm(final_dict):

    bibtex_structure = {
        "author": [],
        "title": None,
        "pages": None,
        "volume": None,
        "number": None,
        "issue": None,
        "date": None,
        "publisher": None,
        "doi": None,
        "articleno": None,
        "additionalinfo": None,
    }

    print("hello", format_date(final_dict))
    bibtex_structure["author"] = extract_authors(final_dict["author"])
    bibtex_structure["title"] = final_dict["title"] if "title" in final_dict else None
    bibtex_structure["pages"] = final_dict["pages"] if "pages" in final_dict else None
    bibtex_structure["volume"] = final_dict["volume"] if "volume" in final_dict else None
    bibtex_structure["number"] = final_dict["number"] if "number" in final_dict else None
    bibtex_structure["issue"] = final_dict["issue"] if "issue" in final_dict else None
    bibtex_structure["date"] = format_date(final_dict) 
    bibtex_structure["publisher"] = final_dict["publisher"] if "publisher" in final_dict else None
    bibtex_structure["doi"] = final_dict["url"] if "url" in final_dict else None
    bibtex_structure["articleno"] = final_dict["articleno"] if "articleno" in final_dict else None


    print(bibtex_structure)
    return bibtex_structure

def parseIEEE(final_dict):

    bibtex_structure = {
        "author": [],
        "title": None,
        "pages": None,
        "volume": None,
        "number": None,
        "issue": None,
        "date": None,
        "publisher": None,
        "doi": None,
        "articleno": None,
        "additionalinfo": None,
    }


    # print("gg",final_dict["author"].replace("\n"," "))
    bibtex_structure["author"] = extract_authors(final_dict["author"].replace("\n"," "))
    bibtex_structure["title"] = final_dict["title"] if "title" in final_dict else None
    bibtex_structure["pages"] = final_dict["pages"] if "pages" in final_dict else None
    bibtex_structure["volume"] = final_dict["volume"] if "volume" in final_dict else None
    bibtex_structure["number"] = final_dict["number"] if "number" in final_dict else None
    bibtex_structure["issue"] = final_dict["issue"] if "issue" in final_dict else None
    bibtex_structure["date"] = format_date(final_dict) 
    bibtex_structure["publisher"] = final_dict["journal"] if "journal" in final_dict else None
    bibtex_structure["doi"] = final_dict["url"] if "url" in final_dict else None
    bibtex_structure["articleno"] = final_dict["articleno"] if "articleno" in final_dict else None


 
    return bibtex_structure

@router.post("/get_bibtex")
async def test2(request_data: MyDataModel):
    try:

        bibtex_structure = {
            "author": [],
            "title": None,
            "pages": None,
            "volume": None,
            "number": None,
            "issue": None,
            "date": None,
            "publisher": None,
            "doi": None,
            "articleno": None,
            "additionalinfo": None,
        }

        bibtexType = "IEEE"
   

        final_dict =  json.loads(request_data.key1)
        print("dict",final_dict)
        # processed_bibtex = process_bibtex(final_dict)




        # bibtex_structure["Additional Info"] = final_dict["abstract"] if "abstract" in final_dict else None
        # # Convert BibtexModel to dictionary
        
        ans = None 
        if bibtexType=="ACM":
            ans = parseAcm(final_dict)

        elif bibtexType=="IEEE":
            ans = parseIEEE(final_dict)

       
        return ans
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


# async def get_professor_by_name(name: str = Query(..., title="Professor Name")):
#     try:
#         professor = prof_collection.find_one({"name": name})

#         if professor:
#             serialized_professor = individual_serial(professor)  # Serialize professor document
#             return serialized_professor
#         else:
#             raise HTTPException(status_code=404, detail=f"Professor with name '{name}' not found")
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail=str(e))
    
    
async def get_professor_by_name(name: str = Query(..., title="Professor Name")):
    try:
        professor = prof_collection.find_one({"name": name})

        if professor:
            return professor
        else:
            raise HTTPException(status_code=404, detail=f"Professor with name '{name}' not found")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

async def get_author_by_name(name:str = Query(..., title="Author Name")):
    try: 
        author = authors_collection.find_one({"authorName":name})
        
        if author:
            return author
        else:
            raise HTTPException(status_code=404, detail=f"Author with name '{name}' not found")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit_form")
async def submitForm(request_data: MyDataModel):
    try:
        final_dict =  json.loads(request_data.key1)
        paper = researchPaper()
        paper.title = final_dict["title"]
        paper.pages = final_dict["pages"]
        paper.volume = final_dict["volume"]
        paper.number = final_dict["number"]
        paper.issue = final_dict["issue"]
        paper.date = final_dict["date"]
        paper.publisher = final_dict["publisher"]
        paper.doi = final_dict["doi"]
        paper.articleno = final_dict["articleno"]
        paper.paperId = generate_user_id(8) 
        


        paper.authors = []
        paper_authors = []
        
        for i in final_dict['author']:
            try:
                temp = await get_author_by_name(i['name'])
                temp['papers'].append(paper.paperId)
                authors_collection.update_one({'authorId': temp['authorId']}, {'$set': {'papers': temp['papers']}})
                # paper_authors.append(temp)
                paper.authors.append(temp['authorId'])
            except Exception as e:
                new_author = paperAuthor()
                new_author.authorName = i['name']
                new_author.designation = i['designation']
                new_author.papers = []
                new_author.papers.append(paper.paperId)
                
                new_author.authorId = generate_user_id()

                if(new_author.designation == 'IIITD Faculty'):
                    auth = await get_professor_by_name(new_author.authorName)

                    new_author.authorId =  auth["profId"]
                    
                # paper_authors.append(new_author)
                paper.authors.append(new_author.authorId)
                authors_collection.insert_one(new_author.__dict__)

            
                
        # paper.authors = [author.authorId for author in paper_authors]
        papers_collection.insert_one(paper.__dict__)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/papersByPublisher")
async def get_papers_by_publisher(publisher_name: str = Query(..., title="Publisher Name")):
    try:
        # Query the database for papers by the specified publisher
        papers = research_paper_list_serial(
            papers_collection.find({"publisher": publisher_name})
        )
        
        if not papers:
            raise HTTPException(status_code=404, detail=f"No papers found for publisher '{publisher_name}'")
        
        return papers
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))    

def generate_publication_time_period(start_date_time, end_date_time):
    # Convert the input date-time strings to datetime objects
   
    # Define month names for formatting
    month_names = ["January", "February", "March", "April", "May", "June", "July",
                   "August", "September", "October", "November", "December"]
    
    # Format the start and end dates
    start_month_name = month_names[start_date_time.month - 1]
    end_month_name = month_names[end_date_time.month - 1]
    start_date_str = f"{start_month_name} {start_date_time.day}, {start_date_time.year}"
    end_date_str = f"{end_month_name} {end_date_time.day}, {end_date_time.year}"
    
    # Generate the publication time period string
    publication_time_period = f"(PUBLISHED BETWEEN {start_date_str.upper()} AND {end_date_str.upper()})"
    
    return publication_time_period

def generate_pdf(prof_detail, research_contributions, pdf_filename):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    print("prof_da:", prof_detail)
    
    prof_data = prof_detail[0]
    research_data = research_contributions[0]
    
   
    c.setFont("Helvetica", 12)
    print("gg")
    # Academic Year and Professor's Name
    
    top_pos = 750
    left_pos = 80
    copy_top_pos = top_pos
    academic_year = f"{get_current_academic_year()}, {prof_data['name']}"
    c.drawString(left_pos, top_pos, academic_year)

    
    # logo_url = "https://i.ibb.co/dmNNpc0/IIITD-Email-Footer.png"
    # response = requests.get(logo_url)
    # if response.status_code == 200:
    #     logo_image = Image(BytesIO(response.content))
    #     logo_image.drawHeight = 30  # Set the height of the logo image
    #     logo_image.drawWidth = 100   # Set the width of the logo image
    #     logo_image.wrapOn(c, 100, 90)  # Wrap the image to a specific size
    #     logo_image.drawOn(c, 400, 740)  # Position the image to the right of the heading

    
    changeFontToCyan(c)
    detail_title = "Details about the faculty member"
    c.drawString(left_pos, top_pos-20, detail_title)
    
    changeFontToBlack(c)

    # PhD Year
    phd_year = f"PhD (Year): {prof_data['phdYear']}"
    top_pos = top_pos-50
    c.drawString(left_pos, top_pos , phd_year)

    # Date of Joining
    date_of_joining = f"Date of Joining IIIT-Delhi: {prof_data['dateOfJoining']}"
    top_pos = top_pos-15
    c.drawString(left_pos, top_pos, date_of_joining)

    # Primary Department
    primary_dept = f"Primary Department: {prof_data['primaryDept']}"
    top_pos = top_pos-15
    c.drawString(left_pos, top_pos, primary_dept)

    # Broad Research Domain
    
    c.setFont("Helvetica-Bold", 10)  # Set the font to bold
    research_domain_label = "Broad Research Domain:"
    top_pos = top_pos-15
    c.drawString(left_pos, top_pos, research_domain_label)  
    string_res = ", ".join(prof_data["BroadRsrchDomain"])
    c.drawString(left_pos+125, top_pos, string_res)

    c.setFont("Helvetica", 10)  # Reset the font to regular
    top_pos = top_pos-30
    c.line(left_pos, top_pos, 550, top_pos) #breakline
    
   
    
    if(research_data):
        print("research_data", research_data)
        changeFontToCyan(c)
        top_pos = top_pos-20
        
        research_heading = "Research Contributions (Research, Development and Innovation)"
        c.drawString(left_pos, top_pos, research_heading)
        
        top_pos = top_pos-15
        c.setFont("Helvetica", 10)
        publication_heading = "Publications"
        c.drawString(left_pos, top_pos, publication_heading)
        
        changeFontToBlack(c)
        top_pos = top_pos-20
        c.setFont("Helvetica-Bold", 10)
        note_heading = "Full-length Journal Papers"
        c.drawString(left_pos, top_pos, note_heading)
        
        top_pos = top_pos - 20

        datesList = ["2021-05-01", "2022-05-01","2023-05-01","2024-05-01" ]
        datesList1 = ["2022-05-01", "2023-05-01","2024-05-01","2025-05-01" ]
        
        data = []
        # for i in range(len(datesList)):
        #     time_period = get_publications_in_date_range(research_contributions,datesList[i],datesList1[i])
        #     data.append(time_period)
        
        print("data: ", data)
        publication_time_period = f"(PUBLISHED BETWEEN {datesList[0]} AND {datesList1[1]})"
        changeFontToBlack(c)

        c.drawString(left_pos, top_pos, publication_time_period)
        top_pos = top_pos - 20

        # title =  ", ".join(research_data["coAuthors"]) + ". "+ research_data["title"]
        # Assuming `research_data` is an instance of the `researchContributions` Pydantic model
        co_author_names = [co_author["name"] for co_author in research_data["coAuthors"]]
        co_author_names_string = ", ".join(co_author_names)
        title = f"{co_author_names_string}. {research_data['title']}"

        title = textwrap.wrap(title, width=80)  # Adjust width as needed
        print(title)
        # Print each line of the note
        for i in title:
            c.drawString(left_pos+30, top_pos, i)
            top_pos = top_pos - 15  # Decrease top_pos for the next line
        
        
        
        
    # Save the PDF
    c.save()