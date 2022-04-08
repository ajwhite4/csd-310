'''
Andrew White
7 April 2022
Module 5.3 Assignment Part 2
'''

from pymongo import MongoClient

url = "mongodb+srv://admin:admin@cluster0.v9e5p.mongodb.net/pytech?retryWrites=true&w=majority";
client = MongoClient(url)
db = client.pytech

print('-- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --')

student_docs = db.students.find()
for s in student_docs:
    print('Student ID: {0}\nFirst Name: {1}\nLast Name: {2}\n'.format(s['student_id'],
        s['first_name'], s['last_name']))



print('\n-- DISPLAYING STUDENT DOCUMENT FROM find_one() QUERY --')

student_doc = db.students.find_one({'student_id': 1008})
print('Student ID: {0}\nFirst Name: {1}\nLast Name: {2}\n'.format(student_doc['student_id'],
        student_doc['first_name'], student_doc['last_name']))


input('\n\nEnd of program, press any key to exit... ')
