'''
Andrew White
7 April 2022
Module 5.3 Assignment Part 1
'''

from pymongo import MongoClient

url = "mongodb+srv://admin:admin@cluster0.v9e5p.mongodb.net/pytech?retryWrites=true&w=majority";
client = MongoClient(url)
db = client.pytech

print("-- INSERT STATEMENTS --")

new_student_object = { 
    "student_id": 1007, 
    "first_name": "Thorin", 
    "last_name": "Oakenshield"
    }

new_student_Id = db.students.insert_one(new_student_object).inserted_id
print("Inserted student record Thorin Oakenshield into the students collection with document_id " + str(new_student_Id))

new_student_object = { 
    "student_id": 1008, 
    "first_name": "Bilbo", 
    "last_name": "Baggins"
    }

new_student_Id = db.students.insert_one(new_student_object).inserted_id
print("Inserted student record Bilbo Baggins into the students collection with document_id " + str(new_student_Id))

new_student_object = { 
    "student_id": 1009, 
    "first_name": "Frodo", 
    "last_name": "Baggins"
    }

new_student_Id = db.students.insert_one(new_student_object).inserted_id
print("Inserted student record Frodo Baggins into the students collection with document_id " + str(new_student_Id))


input("\n\nEnd of program, press any key to exit... ")
