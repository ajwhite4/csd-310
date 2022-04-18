'''
Andrew White
17 April 2022
Module 6.2 Assignment
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

updateQuery = { 'student_id': 1007 }
updateValues = { '$set': { 'last_name': 'Oakenshield II' } }

db.students.update_one(updateQuery, updateValues)

print('\n-- DISPLAYING STUDENT DOCUMENT 1007 --')

student_doc = db.students.find_one({'student_id': 1007})
print('Student ID: {0}\nFirst Name: {1}\nLast Name: {2}\n'.format(student_doc['student_id'],
        student_doc['first_name'], student_doc['last_name']))


input("\n\nEnd of program, press any key to continue... ")
