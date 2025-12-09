from pymongo import MongoClient

client = MongoClient("mongodb+srv://hemantpb123_db_user:nFRetGlTYGg2Zajd@project2.nf6npg4.mongodb.net/?retryWrites=true&w=majority")
db = client["CollegeDB"]
collection = db["Students"]

result = collection.update_one(
    {"name": "Aarav"},
    {"$set": {"marks": 95}}
)

print("Modified Count:", result.modified_count)
