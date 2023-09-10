from pymongo import MongoClient

client = MongoClient("mongodb+srv://mv19082001:ETkKgpNBEeWhxDjg@cluster0.yfygq7j.mongodb.net/?retryWrites=true&w=majority")

db = client.annual_insight  

collection_name = db["annual_insight_collection"]
