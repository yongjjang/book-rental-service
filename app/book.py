from .process_data import *
from .models import *
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify

book = Blueprint('book', __name__, url_prefix='/book', template_folder='templates/book/', static_folder='static')


@book.route('/search')
def search():
    item = get_tables(Book)
    item_size = len(item[0])

    return render_template('book/book_search.html', items=item, length_item=item_size, table_head=Book.column_list)


@book.route('/info', methods=['POST'])
def info():
    bookname = request.form['bookname']
    author = request.form['author']
    is_valid = False

    item = Book.query.filter(Book.name.ilike("%" + bookname + "%")).filter(
        Book.author.ilike("%" + author + "%")).first()

    if item:
        is_valid = True
    return render_template('book/book_info.html', entry=item, is_valid=is_valid)


@book.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        id = get_max_id(Book) + 1
        bookname = request.form['bookname']
        author = request.form['author']
        isbn = request.form['isbn']
        price = request.form['price']
        description = request.form['description']
        link = request.form['link']
        picture = request.form['Picture']

        if add_entry(Book(id, isbn, bookname, author, price, description, link, picture, True)):
            return render_template('/success_or_failed.html', status="Success", description="도서 등록 성공!")
        else:
            return render_template('/success_or_failed.html', status="Failed", description="도서 등록 실패")
    else:
        return render_template('/book/book_register.html')


@book.route('/check', methods=['POST'])
def check_valid():
    data = request.get_json()
    isbn = data['isbn']

    logging.info("new isbn :" + isbn)
    result = Book.query.filter_by(isbn=isbn).first()

    if not result:
        logging.info(isbn + ' 존재하지 않는 도서')
        return jsonify({'existence': 'false'})
    else:
        logging.info(isbn + ' 존재하는 도서')
        return jsonify({'existence': 'true'})


@book.route('/get_json', methods=['POST'])
def get_json_book():
    data = request.get_json()
    isbn = data['isbn']

    result = Book.query.filter(isbn == isbn).first()
    result = {'bookName': result.name, 'author': result.author}

    if not result:
        return "false"
    else:
        return jsonify(result)


@book.route('/delete', methods=['POST'])
def delete():

        isbn = request.form['isbn']
        try:
            Book.query.filter(Book.isbn == isbn).delete(synchronize_session=False)
            logging.info("Delete Success : " + isbn)
            db_session.commit()
            return render_template('/success_or_failed.html', status="Success", description="도서 삭제 성공!")
        except Exception as ex:
            logging.info(ex)
            return render_template('/success_or_failed.html', status="Failed", description="도서 삭제 실패 : " + ex)


@book.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        try:
            isbn = request.form['isbn']
            bookname = request.form['bookname']
            author = request.form['author']
            price = request.form['price']
            description = request.form['description']
            link = request.form['link']
            picture = request.form['picture']

            filtered_book = Book.query.filter(Book.isbn == isbn).first()
            # Book.query.update(values={name=bookname, author=author, price=price, description=description, link=link,
            #                      picture=picture}).where(Book.isbn==isbn))
            # Book.query.update(values={'name':bookname}, where(Book.isbn==isbn))
            filtered_book.name = bookname
            filtered_book.author = author
            filtered_book.price = price
            filtered_book.description = description
            filtered_book.link = link
            filtered_book.picture = picture
            db_session.flush()
            db_session.commit()
            return render_template('/success_or_failed.html', status="Success", description="도서 정보 수정 성공!")
        except Exception as ex:
            return render_template('/success_or_failed.html', status="Failed", description="도서 정보 수정 실패 : " + str(ex))
    else:
        return render_template('/book/book_update.html')
