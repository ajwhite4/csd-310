'''
Andrew White
28 April 2022
Module 12.3 Assignment
'''

from ast import Try
from asyncio.windows_events import NULL
from msilib.schema import Error
from sqlite3 import connect
import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}

#display main menu
def show_menu():
    #while loop to ensure a valid option is selected
    while True:
        try:
            print("\n-- MAIN MENU --\n1. View Books\n2. View Store Locations\n3. My Account\n4. Exit Program")
            option = int(input("\nSelect a menu option: "))
            if option > 4 or option < 1:
                print("\nInvalid Entry.")
            else:
                return option
        except:
            print("\nInvalid Entry.")

#display account menu
def show_account_menu():
    #while loop to ensure a valid option is selected
    while True:
        try:
            print("\n-- ACCOUNT MENU --\n1. Wishlist\n2. Add Book\n3. Main Menu")
            acctOpt = int(input("\nSelect an option: "))
            if acctOpt > 3 or acctOpt < 1:
                print("\nInvalid Entry.")
            else:
                return acctOpt
        except:
            print("\nInvalid Entry.")

#display location ID and address
def show_locations(_cursor):
    #query to get location info
    _cursor.execute('SELECT store_id, locale, hours '+
                    'FROM store')
    stores = _cursor.fetchall()
        
    print('\n-- STORE LOCATIONS --')

    #parse through and print query results
    for store in stores:
        print('Store ID: {}\nAddress:  {}\nHours:    {}\n'.format(store[0], store[1], store[2]))


#display books that store carries
def show_books(_cursor):
    #query to get book details
    _cursor.execute('SELECT book_name, author, details '+
                    'FROM book')
    books = _cursor.fetchall()
      
    print('\n-- BOOKS IN STOCK --')

    #parse through and print details for all books
    for book in books:
        print('Title: {}\nAuthor: {}\nSynopsis: {}\n'.format(book[0], book[1], book[2]))


#validate that user exists
def validate_user():
    try:
        #capture customer ID
        while True:
            try:
                userId = int(input("\nPlease enter your user ID: "))
                break
            except:
                print("\nInvalid Entry.")

        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        #query to validate that user exists
        cursor.execute('SELECT user_id, first_name, Last_name '+
                       'FROM user '+
                       'WHERE user_id = {}'.format(userId))
        users = cursor.fetchall()
        
        #check results of query to see if user exists and display appropriate message
        if cursor.rowcount == 0:
            print('\nAccount not found. Returning to main menu...')
            authFlag = False
        else:
            for user in users:
                print('\nYou have successfully logged in {} {}'.format(user[1], user[2]))
            authFlag = True

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("The supplied username or password are invalid")

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("The specified database does not exist")

        else:
            print(err)

    finally:
        db.close()
        #return auth results and userID
        return authFlag, userId

#display users wishlist books
def show_wishlist(_cursor,_userId):
    #query to select all books in users wishlist
    _cursor.execute('SELECT book.book_id, book_name, author, details FROM wishlist '+
                    'INNER JOIN book ON wishlist.book_id = book.book_id '+
                    'INNER JOIN user ON wishlist.user_id = user.user_id '+
                    'WHERE wishlist.user_id = {}'.format(_userId))
    wishlist = _cursor.fetchall()
        
    #check query results and print info for each book in wishlist
    if _cursor.rowcount == 0:
        print('\nThere are no books currently on your wishlist')
    else:
        print('\n-- YOUR WISHLIST --')
        for book in wishlist:
            print('Title: {}\nAuthor: {}\nSynopsis: {}\n'.format(book[1], book[2], book[3]))


#display books that are carried in store that are not in users wishlist
def show_books_to_add(_cursor,_userId):
    #query books that are not in users wishlist
    _cursor.execute('SELECT book_id, book_name, author, details '+
                    'FROM book '+
                    'WHERE book_id NOT IN ('+
                        'SELECT book_id '+
                        'FROM wishlist '+
                        'WHERE user_id = {})'.format(_userId))
    books = _cursor.fetchall()
        
    #check query results and display each book
    if _cursor.rowcount == 0:
        print('\nThere are no books available to add to your wishlist.')
        return NULL
    else:
        print('\n-- AVAILABLE BOOKS --')
        for book in books:
            print('Book ID: {}\nTitle: {}\nAuthor: {}\nSynopsis: {}\n'.format(book[0], book[1], book[2], book[3]))

        while True:
            try:
                bookId = int(input("Select a book ID to add to your wishlist: "))
                return bookId
            except:
                print("\nInvalid Entry.\n")

#check to ensure selected book is not in wishlist and if not add it to the wishlist
def add_book_to_wishlist(_cursor,_bookId,_userId):
    #query to check if book is already in users wishlist
    _cursor.execute('SELECT book_id '+
                    'FROM book '+
                    'WHERE book_id NOT IN ('+
                        'SELECT book_id '+
                        'FROM wishlist '+
                        'WHERE user_id = {}) AND book_id = {}'.format(_userId, _bookId))
    books = _cursor.fetchall()

    #check results of query
    if _cursor.rowcount == 0:
        print('\nInvalid Selection.\n')
    else:
        _cursor = db.cursor()
        #if book is not in wishlist, insert the book into wishlist
        _cursor.execute('INSERT INTO wishlist (user_id, book_id) '+
                        'VALUES ({}, {})'.format(_userId, _bookId))
         
        #check to make sure book was added to wishlist successfully
        if _cursor.rowcount == 1:
            db.commit()
            print('\nThe selected book has successfully been added to your wishlist.')
        else:
            print('\nSorry, we were unable to add that book to your wishlist.')


#Main Application Code
try:
    #set up database connection
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    
    option = show_menu()

    while option != 4:
        if option == 1:
            #View Books
            show_books(cursor)
        elif option == 2:
            #View Locations
            show_locations(cursor)
        elif option == 3:
            #User Account
            result = validate_user()
            authFlag = result[0]
            userId = result[1]
            
            if(authFlag):
                #ensure valid input for account menu
                acctOpt = show_account_menu()

                while acctOpt != 3:
                    if acctOpt == 1:
                        #Wishlist
                        show_wishlist(cursor, userId)
                    elif acctOpt == 2:
                        #Add Book
                        bookId = show_books_to_add(cursor, userId)
                        if bookId != NULL:
                            add_book_to_wishlist(cursor, bookId, userId)

                    acctOpt = show_account_menu()

        option = show_menu()
    

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
    else:
            print(err)

finally:
    print("\nThank you, Goodbye!\n\n")
    db.close()