from .database import db_session, init_db
from .models import User, Book, BookRental
from sqlalchemy import func
import datetime
import logging

init_db()


def get_tables(db_table):
    """
        @author : TAEYONG LEE
        :param db_table: database table in model.py
        :type db_table: database model Object
        :return type: list[list]
    """
    entries = []
    queries = db_session.query(db_table)

    for q in queries:
        s = str(q).split('|')
        entries.append(s)

    return entries


def add_entry(entry):
    """
        @author : TAEYONG LEE
        :param entry: database table in model.py
        :type entry: database model Object ex) User(param..), Book(params..) etc..

        :return Returns True if the operation succeeds, False if it fails

        :usage
        user = User(id, name...)
        add_entry(user)
    """
    try:
        db_session.add(entry)
        db_session.commit()
    except Exception as ex:
        print(ex)
        return False

    logging.info("Database : Add Entry Success")
    logging.info(str(entry).split('|'))
    return True


def delete_entry(db_table, id):
    """
        @author : TAEYONG LEE
        :param db_table: database table in model.py
        :type db_table: database model Object

        :param id: database model entry's id
        :type id: int

        :return Returns True if the operation succeeds, False if it fails

        :usage
        delete_entry(User, 100)
    """
    try:
        db_session.query(db_table).filter(db_table.id == id).delete()
        db_session.commit()
    except Exception as ex:
        print(ex)
        return False

    logging.info("Database : Delete Entry Success")
    return True


def search_entry(db_table, condition, keyword):
    """
        @author : TAEYONG LEE
        :param db_table: database table in model.py
        :type db_table: database model Object

        :param condition: search condition. ex)User.name
        :type condition: db_table.column

        :param keyword: search keyword. ex)"Lee"
        :type keyword: str or int

        :return filtered table.


        :usage
        **if keyword is str**
        entry = search_entry(User, User.name, "yongjjang")

        **if keyword is int**
        entry = search_entry(User, User.id, 200)
        """

    if type(keyword) is str:
        result = db_session.query(db_table).filter(condition.ilike('%' + keyword + "%")).first()
        entry = str(result).split('|')
        return entry

    elif type(keyword) is int:
        id = keyword
        result = db_session.query(db_table).filter(condition == id).first()
        entry = str(result).split('|')
        return entry


def get_max_id(db_table):
    try:
        return int(db_session.query(func.max(db_table.id)).scalar())
    except:
        return 1




def get_rent_date():
    rental_date = datetime.date.today()
    return_date = rental_date + datetime.timedelta(days=14)
    return str(rental_date), str(return_date)


def parse_row(row):
    return str(row).split('|')


if __name__ == "__main__":
    tst = search_entry(User, User.birthday, "2020%")
    print(tst)

    rst = User.query.all()
    ra = Book.query.filter(Book.name.like("asdasdasd")).all()

    if not ra:
        print("HI")
    # user = User(101, 'yong', '1995-10-06', 'M', 'yongjjang@walking_potato', '010-1234-1231', 'static/images/testImage', True)
    # add_entry(user)
    #
    # if delete_entry(User, 101):
    #     logging.info("삭제 성공")
    # else:
    #     logging.info("삭제 실패")
    #
    # max_id = db_session.query(func.max(User.id)).scalar()
    # print(type(max_id), max_id)
    #
    # print(search_entry(User, User.name, "bi"))
    # for q in db_session.query(User).filter(User.name.like('%' + "A" + "%")):
    #     print(q)
    #     print(type(q))
    #
    # result = db_session.query(User).filter(User.id == 1).all()
    #
    # for r in result:
    #     print(r)
    #     print(r.column_list)


