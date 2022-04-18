'''
Andrew White
17 April 2022
Module 6.3 Assignment
'''

from pymongo import MongoClient

url = "mongodb+srv://admin:admin@cluster0.v9e5p.mongodb.net/pytech?retryWrites=true&w=majority";
client = MongoClient(url)
db = client.pytech


print("-- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --")

student_docs = db.students.find()
for s in student_docs:
    print('Student ID: {0}\nFirst Name: {1}\nLast Name: {2}\n'.format(s['student_id'],
        s['first_name'], s['last_name']))


print("\n-- INSERT STATEMENTS --")

new_student_object = { 
    "student_id": 1010, 
    "first_name": "John", 
    "last_name": "Doe"
    }

new_student_Id = db.students.insert_one(new_student_object).inserted_id
print("Inserted student record John Doe into the students collection with document_id " + str(new_student_Id))


print('\n-- DISPLAYING STUDENT TEST DOC --')

student_doc = db.students.find_one({'student_id': 1010})
print('Student ID: {0}\nFirst Name: {1}\nLast Name: {2}\n'.format(student_doc['student_id'],
        student_doc['first_name'], student_doc['last_name']))

updateQuery = { 'student_id': 1010 }
db.students.delete_one(updateQuery)


print("\n-- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --")

student_docs = db.students.find()
for s in student_docs:
    print('Student ID: {0}\nFirst Name: {1}\nLast Name: {2}\n'.format(s['student_id'],
        s['first_name'], s['last_name']))


input("\n\nEnd of program, press any key to continue... ")
