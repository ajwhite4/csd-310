'''
Andrew White
28 April 2022
Module 12.3 Assignment
'''

from ast import Try
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

def show_menu():
    print("\n-- MAIN MENU --")
    print("1. View Books")
    print("2. View Store Locations")
    print("3. My Account")
    print("4. Exit Program")

def show_account_menu():
    print("\n-- ACCOUNT MENU --")
    print("1. Wishlist")
    print("2. Add Book")
    print("3. Main Menu")

def show_locations():
    try:
        db = mysql.connector.connect(**config)

        cursor = db.cursor()
        cursor.execute("SELECT store_id, locale FROM store")
        stores = cursor.fetchall()
        
        print('\n-- STORE LOCATIONS --')

        for store in stores:
            print('Store ID: {}\nAddress: {}\n'.format(store[0], store[1]))

        input("Press any key to return to Main Menu")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  The supplied username or password are invalid")

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("  The specified database does not exist")

        else:
            print(err)

    finally:
        db.close()

def show_books():
    try:
        db = mysql.connector.connect(**config)

        cursor = db.cursor()
        cursor.execute("SELECT book_id, book_name, author, details FROM book")
        books = cursor.fetchall()
        
        print('\n-- BOOKS IN STOCK --')

        for book in books:
            print('Book ID: {}\nTitle: {}\nAuthor: {}\nSynopsis: {}\n'.format(book[0], book[1], book[2], book[3]))

        input("Press any key to return to Main Menu")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  The supplied username or password are invalid")

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("  The specified database does not exist")

        else:
            print(err)

    finally:
        db.close()

def validate_user():
    try:
        db = mysql.connector.connect(**config)
        userId = int(input("\nPlease enter your user ID: "))

        cursor = db.cursor()
        cursor.execute('SELECT user_id, first_name, Last_name FROM user WHERE user_id = {}'.format(userId))
        users = cursor.fetchall()
        
        if cursor.rowcount == 0:
            print('\nAccount not found. Returning to main menu...')
            authFlag = False
        else:
            for user in users:
                print('\nYou have successfully logged in {} {}'.format(user[1], user[2]))
            authFlag = True

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  The supplied username or password are invalid")

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("  The specified database does not exist")

        else:
            print(err)

    finally:
        db.close()
        return authFlag, userId

def show_wishlist(userId):
    try:
        db = mysql.connector.connect(**config)
        
        cursor = db.cursor()
        cursor.execute('SELECT book.book_id, book_name, author, details FROM wishlist INNER JOIN book ON wishlist.book_id = book.book_id INNER JOIN user ON wishlist.user_id = user.user_id WHERE wishlist.user_id = {}'.format(userId))
        wishlist = cursor.fetchall()
        
        if cursor.rowcount == 0:
            print('\nThere are no books currently on your wishlist')
        else:
            print('\n-- YOUR WISHLIST --')
            for book in wishlist:
                print('Book ID: {}\nTitle: {}\nAuthor: {}\nSynopsis: {}\n'.format(book[0], book[1], book[2], book[3]))

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  The supplied username or password are invalid")

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("  The specified database does not exist")

        else:
            print(err)

    finally:
        db.close()

def show_books_to_add(userId):
    try:
        db = mysql.connector.connect(**config)
        
        cursor = db.cursor()
        cursor.execute('SELECT book_id, book_name, author, details FROM book WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})'.format(userId))
        books = cursor.fetchall()
        
        if cursor.rowcount == 0:
            print('\nThere are no books available to add to your wishlist.')
        else:
            print('\n-- AVAILABLE BOOKS --')
            for book in books:
                print('Book ID: {}\nTitle: {}\nAuthor: {}\nSynopsis: {}\n'.format(book[0], book[1], book[2], book[3]))

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  The supplied username or password are invalid")

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("  The specified database does not exist")

        else:
            print(err)

    finally:
        db.close()

def add_book_to_wishlist(bookId, userId):
    try:
        db = mysql.connector.connect(**config)
        
        cursor = db.cursor()
        cursor.execute('SELECT book_id FROM book WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {}) AND book_id = {}'.format(userId, bookId))
        books = cursor.fetchall()

        if cursor.rowcount == 0:
            print('\nInvalid Selection.\n')
            pass
        else:
            db = mysql.connector.connect(**config)
            cursor = db.cursor()
            cursor.execute('INSERT INTO wishlist (user_id, book_id) VALUES ({}, {})'.format(userId, bookId))

            if cursor.rowcount == 1:
                db.commit()
                print('\nThe selected book has successfully been added to your wishlist.')
            else:
                print('\nSorry, we were unable to add that book to your wishlist.')

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  The supplied username or password are invalid")

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("  The specified database does not exist")

        else:
            print(err)

    finally:
        db.close()

#Main Application Code

while True:
    try:
        show_menu()
        option = int(input("\nSelect a menu option: "))
        while option != 4:
            if option == 1:
                #View Books
                show_books()
                pass
            elif option == 2:
                #View Locations
                show_locations()
                pass
            elif option == 3:
                #User Account
                result = validate_user()
                authFlag = result[0]
                userId = result[1]

                if(authFlag):
                    while True:
                        try:
                            show_account_menu()
                            acctOpt = int(input("\nSelect an option: "))
                            while acctOpt != 3:
                                if acctOpt == 1:
                                    #Wishlist
                                    show_wishlist(userId)
                                    pass
                                elif acctOpt == 2:
                                    #Add Book
                                    show_books_to_add(userId)
                                    while True:
                                        try:
                                            bookId = int(input("Select a book ID to add to your wishlist: "))
                                            add_book_to_wishlist(bookId, userId)
                                        except:
                                            print("\nInvalid Option.\n")
                                        finally:
                                            break
                                    pass
                                else:
                                    print("\nInvalid Option.")

                                show_account_menu()
                                acctOpt = int(input("\nSelect a menu option: "))
                        except:
                            print("\nInvalid Option.\n")
                        finally:
                            break

                else:
                    pass
            else:
                print("\nInvalid Option.")

            show_menu()
            option = int(input("\nSelect a menu option: "))
    except:
        print("\nInvalid entry.")
    finally:
        break

print("\nThank you, Goodbye!\n\n")

