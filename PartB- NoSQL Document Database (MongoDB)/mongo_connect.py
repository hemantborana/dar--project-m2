from pymongo import MongoClient

# 1. CONNECT TO MONGODB ATLAS
client = MongoClient("mongodb+srv://hemantpb123_db_user:nFRetGlTYGg2Zajd@project2.nf6npg4.mongodb.net/?retryWrites=true&w=majority&appName=Project2")


# 2. SELECT DATABASE
db = client["Project2_Database"]

# 3. SELECT COLLECTION (TABLE)
students = db["Students"]  

# 4. INSERT SAMPLE DOCUMENT
sample = {
    "name": "Hemant",
    "course": "Data Analytics",
    "marks": 90
}

result = students.insert_one(sample)
print("Inserted ID:", result.inserted_id)

# 5. READ DOCUMENTS
for doc in students.find():
    print(doc)
