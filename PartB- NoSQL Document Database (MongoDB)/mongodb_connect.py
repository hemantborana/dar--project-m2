from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb+srv://hemantpb123_db_user:nFRetGlTYGg2Zajd@project2.nf6npg4.mongodb.net/?retryWrites=true&w=majority&appName=Project2")
    db = client["CollegeDB"]
    return db
