from pymongo import MongoClient

# client = MongoClient("mongodb+srv://mv19082001:ETkKgpNBEeWhxDjg@cluster0.yfygq7j.mongodb.net/?retryWrites=true&w=majority")

client = MongoClient("mongodb+srv://mohit20085:GmyeNLjV5xTNsaZT@clusterip.yeitqcb.mongodb.net/")

db = client.annual_insight  

prof_collection = db["prof_collection"]
research_collection = db["research_collection"]