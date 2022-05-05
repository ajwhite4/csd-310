
-- drop test user if exists 
DROP USER IF EXISTS 'whatabook_user'@'localhost';


-- create pysports_user and grant them all privileges to the pysports database 
CREATE USER 'whatabook_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'MySQL8IsGreat!';

-- grant all privileges to the pysports database to user pysports_user on localhost 
GRANT ALL PRIVILEGES ON whatabook.* TO'whatabook_user'@'localhost';


-- drop tables if they are present
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS wishlist;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS book;


-- create the user table 
CREATE TABLE user (
    user_id     INT             NOT NULL        AUTO_INCREMENT,
    first_name  VARCHAR(75)     NOT NULL,
    Last_name   VARCHAR(75)     NOT NULL,
    PRIMARY KEY(user_id)
); 

-- create the book table
CREATE TABLE book (
    book_id     INT             NOT NULL        AUTO_INCREMENT,
    book_name   VARCHAR(200)    NOT NULL,
    details     VARCHAR(500),
    author      VARCHAR(200)    NOT NULL,
    PRIMARY KEY(book_id)
);

-- create the wishlist table and set the foreign key
CREATE TABLE wishlist (
    wishlist_id INT             NOT NULL        AUTO_INCREMENT,
    user_id     INT             NOT NULL,
    book_id     INT             NOT NULL,
    PRIMARY KEY(wishlist_id),
    CONSTRAINT fk_book
    FOREIGN KEY(user_id) 
        REFERENCES user(user_id),
    CONSTRAINT fk_user
    FOREIGN KEY(book_id)
        REFERENCES book(book_id)
);

-- create the store table
CREATE TABLE store (
    store_id    INT             NOT NULL        AUTO_INCREMENT,
    locale      VARCHAR(500)    NOT NULL,
    PRIMARY KEY(store_id)
);


-- insert store records
INSERT INTO store(locale)
    VALUES('12355 W Center Rd, Omaha, NE 68144');

-- insert book records
INSERT INTO book(book_name, details, author) 
    VALUES('Mark of the Hunter', 'A man refuses to rest until he finds his familys killer in this pulse-pounding tale of the American West.', 'Charles G West');

INSERT INTO book(book_name, details, author) 
    VALUES('Breaking Dawn', 'To be irrevocably in love with a vampire is both fantasy and nightmare woven into a dangerously heightened reality for Bella Swan.', 'Stephenie Meyer');

INSERT INTO book(book_name, details, author) 
    VALUES('Different Seasons', 'The bestselling master of horror and suspense offers four new tales of outlandish, commonplace, and surprising terror.', 'Stephen King');

INSERT INTO book(book_name, details, author) 
    VALUES('The Institute', 'As psychically terrifying as Firestarter, and with the spectacular kid power of It, The Institute is Kings gut-wrenchingly dramatic story of good vs. evil in a world where the good guys dont always win.', 'Stephen King');

INSERT INTO book(book_name, details, author) 
    VALUES('The Inn', 'James Pattersons strongest team since the Womens Murder Club are the first responders when their seafront town is targeted by vicious criminals.', 'James Patterson');

INSERT INTO book(book_name, details, author) 
    VALUES('The Runaway', 'When Peter Ash rescues a stranded woman, he finds shes in far deeper trouble than he bargained for.', 'Nick Petrie');

INSERT INTO book(book_name, details, author) 
    VALUES('Beautiful', 'A renowned supermodels world is torn apart in an instant, sending her on an unexpected journey of discovery.', 'Danielle Steel');

INSERT INTO book(book_name, details, author) 
    VALUES('The Maid', 'A charmingly eccentric hotel maid discovers a guest murdered in his bed. Solving the mystery will turn her once orderly world upside down.', 'Nita Prose');

INSERT INTO book(book_name, details, author) 
    VALUES('Verity', 'Lowen Ashleigh is a struggling writer on the brink of financial ruin when she accepts the job offer of a lifetime.', 'Colleen Hoover');

-- insert user records 
INSERT INTO user(first_name, last_name) 
    VALUES('John', 'Doe');

INSERT INTO user(first_name, last_name)
    VALUES('Jane', 'Smith');

INSERT INTO user(first_name, last_name)
    VALUES('Mark', 'Funk');

-- insert wishlist records 
INSERT INTO wishlist(user_id, book_id) 
    VALUES((SELECT user_id FROM user WHERE first_name = 'Mark' AND last_name = 'Funk'), (SELECT book_id FROM book WHERE book_name = 'Mark of the Hunter'));

INSERT INTO wishlist(user_id, book_id) 
    VALUES((SELECT user_id FROM user WHERE first_name = 'Jane' AND last_name = 'Smith'), (SELECT book_id FROM book WHERE book_name = 'Breaking Dawn'));

INSERT INTO wishlist(user_id, book_id)  
    VALUES((SELECT user_id FROM user WHERE first_name = 'John' AND last_name = 'Doe'), (SELECT book_id FROM book WHERE book_name = 'Different Seasons'));
