from mongodb_connect import get_db

db = get_db()
students = db.students

# 1. Creating index on "name"
index_name = students.create_index("name")
print("Created Index:", index_name)

# 2. Creating compound index (name + course)
compound_index = students.create_index([("name", 1), ("course", -1)])
print("Compound Index Created:", compound_index)

# 3. Showing all indexes
print("\nAll Indexes:")
for idx in students.list_indexes():
    print(idx)
