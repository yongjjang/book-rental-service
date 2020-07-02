from .process_data import *
from .models import *
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify

user = Blueprint('user', __name__, url_prefix='/user', template_folder='templates/user', static_folder='static')


@user.route('/search')
def search():
    item = get_tables(User)
    item_size = len(item[0])

    return render_template('user/user_search.html',
                           items=item, length_item=item_size,
                           table_head=User.column_list)


@user.route('/info', methods=['POST'])
def info():
    if request.method == 'POST':
        name = request.form['username']
        birthday = request.form['birthday']
        is_valid = False

        item = User.query.filter(User.name.ilike("%" + name + "%")).\
            filter(User.birthday == birthday).first()

        if item:
            is_valid = True

        return render_template('user/user_info.html', entry=item, is_valid=is_valid)


@user.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        id = get_max_id(User) + 1
        username = request.form['username']
        birthday = request.form['birthday']
        email = request.form['email']
        gender = request.form['gender']
        tel = request.form['tel']
        picture = request.form['picture']

        filtered_user = User.query.filter_by(name=username).filter_by(birthday=birthday).first()

        if filtered_user:
            return render_template('/success_or_failed.html', status="Failed", description="사용자 추가 실패..")
        else:
            add_entry(User(id, username, birthday, gender, email, tel, picture, True))
            return render_template('/success_or_failed.html', status="Success", description="사용자 추가 성공!")
    else:
        return render_template('user/user_register.html')


@user.route('/check', methods=['POST'])
def check_valid():
    data = request.get_json()
    username = data['username']
    birthday = data['birthday']

    logging.debug("new name :" + username)
    result = User.query.filter_by(name=username).filter_by(birthday=birthday).first()

    if not result:
        logging.info(username + ' : 사용자 계정 존재하지 않음')
        return jsonify({'existence': 'false'})
    else:
        logging.info(username + ' 사용자 계정 존재함')
        return jsonify({'existence': 'true'})


@user.route('/delete', methods=['POST'])
def delete():
    username = request.form['username']
    birthday = request.form['birthday']
    try:
        user = User.query.filter(User.name.like(username),
                                 User.birthday == birthday).first()
        add_entry(LeavedUser(user.id, user.name, user.birthday,
                             user.gender, user.email, user.telno, user.picturepath, str(datetime.date.today())))
        userid = user.id
        db_session.query(User).filter(User.id == userid).delete(synchronize_session=False)
        db_session.commit()
        return render_template('/success_or_failed.html', status="Success", description="사용자 삭제 성공!")
    except Exception as ex:
        logging.info(ex)
        return render_template('/success_or_failed.html', status="Failed", description="사용자 삭제 실패")


"""
TODO
도서 수정 소스 참고하여 유저 수정 기능 구현
반납 기능 구현
사용자 정보 검색 폼 구현

"""


@user.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        try:
            username = request.form['isbn']
            gender = request.form['gender']
            email = request.form['email']
            telno = request.form['telno']
            birthday = request.form['birthday']
            picturepath = request.form['picturepath']

            filtered_user = User.query.filter_by(name=username).\
                filter_by(birthday=birthday).first()

            filtered_user.name = username
            filtered_user.author = gender
            filtered_user.price = email
            filtered_user.description = telno
            filtered_user.link = picturepath

            db_session.flush()
            db_session.commit()

            return render_template('/success_or_failed.html', status="Success", description="사용자 정보 수정 성공!")
        except Exception as ex:
            return render_template('/success_or_failed.html', status="Failed", description="사용자 정보 수정 실패 : " + str(ex))
    else:
        return render_template('/user/user_update.html')


@user.route('/leaved')
def leaved_search():
    item = get_tables(LeavedUser)
    item_size = len(item[0])

    return render_template('user/user_search.html',
                           items=item, length_item=item_size,
                           table_head=LeavedUser.column_list)