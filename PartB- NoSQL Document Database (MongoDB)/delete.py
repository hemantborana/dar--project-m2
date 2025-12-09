from pymongo import MongoClient

client = MongoClient("mongodb+srv://hemantpb123_db_user:nFRetGlTYGg2Zajd@project2.nf6npg4.mongodb.net/?retryWrites=true&w=majority")
db = client["CollegeDB"]
collection = db["Students"]

result = collection.delete_one({"name": "Ankit"})
print("Deleted Count:", result.deleted_count)
