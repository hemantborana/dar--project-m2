from pymongo import MongoClient

client = MongoClient("mongodb+srv://hemantpb123_db_user:nFRetGlTYGg2Zajd@project2.nf6npg4.mongodb.net/?retryWrites=true&w=majority")
db = client["CollegeDB"]
collection = db["Students"]


many_students = [
    {"name": "Aarav", "course": "Data Analytics", "marks": 85},
    {"name": "Riya", "course": "Computer Science", "marks": 92},
    {"name": "Ankit", "course": "Machine Learning", "marks": 78},
    {"name": "Sara", "course": "Data Analytics", "marks": 88}
]

result = collection.insert_many(many_students)
print("Inserted IDs:", result.inserted_ids)
