from sqlalchemy import Column, Integer, String, Date, Boolean
from .database import base, db_session
import datetime


class Book(base):
    __tablename__ = 'book'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    isbn = Column(String(40))
    name = Column(String(40))
    author = Column(String(40))
    price = Column(String(10))
    description = Column(String(40))
    link = Column(String(100))
    picturepath = Column(String(60))
    isrentedout = Column(Boolean(), default=True)
    column_list = ['ID', 'ISBN', 'Name', 'Author', 'Price', 'Description', 'link', 'Picture', 'Is Rent Out?']

    def __init__(self, id, isbn, name, author, price, description, link, picture_path, isrentedout):
        self.id = id
        self.isbn = isbn
        self.name = name
        self.author = author
        self.price = price
        self.description = description
        self.link = link
        self.picturepath = picture_path
        self.isrentedout = isrentedout

    def __repr__(self):
        return "%d|%s|%s|%s|%s|%s|%s|%s|%s" % \
               (self.id, self.isbn, self.name, self.author, self.price
                , self.description, self.link, self.picturepath, self.isrentedout)


class User(base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    birthday = Column(Date)
    gender = Column(String(2))
    email = Column(String(20))
    telno = Column(String(14))
    picturepath = Column(String(100))
    canrent = Column(Boolean(), default=True)
    column_list = ['ID', 'Name', 'Birthday', 'Gender', 'E-Mail', 'Tel', 'Picture', 'CanRent']

    def __init__(self, id, name, birthday, gender, email, telno, picturepath, canrent):
        self.id = id
        self.name = name
        self.birthday = birthday
        self.gender = gender
        self.email = email
        self.telno = telno
        self.picturepath = picturepath
        self.canrent = canrent

    def __str__(self):
        return "%d|%s|%s|%s|%s|%s|%s|%s" % \
               (self.id, self.name, self.birthday, self.gender, self.email
                , self.telno, self.picturepath, self.canrent)


class BookRental(base):
    __tablename__ = 'bookrental'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    bookid = Column(Integer)
    rentaldate = Column(Date)
    returndate = Column(Date)
    isrentout = Column(Boolean(), default=False)
    column_list = ['ID', 'User ID', 'Book ID', 'Rental Date', 'Return Date', 'Is Rent Out?']

    def __init__(self, id, userid, bookid, rentaldate, returndate, isrentout):
        self.id = id
        self.userid = userid
        self.bookid = bookid
        self.rentaldate = rentaldate
        self.returndate = returndate
        self.isrentout = isrentout

    def __str__(self):
        return "%d|%d|%d|%s|%s|%s" % \
               (self.id, self.userid, self.bookid, self.rentaldate
                , self.returndate, self.isrentout)


class LeavedUser(base):
    __tablename__ = 'leaveduser'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    birthday = Column(Date)
    gender = Column(String(2))
    email = Column(String(20))
    telno = Column(String(14))
    picturepath = Column(String(100))
    leavedate = Column(Date())
    column_list = ['ID', 'Name', 'Birthday', 'Gender', 'E-Mail', 'Tel', 'Picture', 'Leave Date']

    def __init__(self, id, name, birthday, gender, email, telno, picturepath, leavedate):
        self.id = id
        self.name = name
        self.birthday = birthday
        self.gender = gender
        self.email = email
        self.telno = telno
        self.picturepath = picturepath
        self.leavedate = leavedate

    def __str__(self):
        return "%d|%s|%s|%s|%s|%s|%s|%s" % \
               (self.id, self.name, self.birthday, self.gender, self.email
                , self.telno, self.picturepath, self.leavedate)
