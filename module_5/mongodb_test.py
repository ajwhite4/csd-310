'''
Andrew White
7 April 2022
Module 5.2 Assignment
'''

from pymongo import MongoClient

url = "mongodb+srv://admin:admin@cluster0.v9e5p.mongodb.net/pytech?retryWrites=true&w=majority";
client = MongoClient(url)
db = client.pytech

print(" -- Pytech COllection List --")
print(db.list_collection_names())

input("\n\n  End of program, press any key to exit... ")
