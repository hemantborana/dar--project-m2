from mongodb_connect import get_db

db = get_db()
students = db.Students  # Access the "Students" collection

# 1. Counting how many students in each course
pipeline1 = [
    {"$group": {"_id": "$course", "total_students": {"$sum": 1}}}
]
print("\nStudents per Course:")
for row in students.aggregate(pipeline1):
    print(row)

# 2. Average marks by course
pipeline2 = [
    {"$group": {"_id": "$course", "average_marks": {"$avg": "$marks"}}}
]
print("\nAverage Marks per Course:")
for row in students.aggregate(pipeline2):
    print(row)

# 3. Students scoring above 90
pipeline3 = [
    {"$match": {"marks": {"$gt": 90}}},
    {"$project": {"name": 1, "course": 1, "marks": 1}}
]
print("\nStudents Above 90 Marks:")
for row in students.aggregate(pipeline3):
    print(row)