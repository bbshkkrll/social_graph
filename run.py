import json

from flask import request, render_template, make_response, redirect, url_for, jsonify, session

from app import app, app_session, db_session
from app.models import Token, User
from app.modules.vk_exception import VkException
from sqlalchemy.exc import NoResultFound


@app.route("/graph")
def graph():
    if 'vk_user_id' in session:
        return render_template('index.html')
    try:
        code = session['code']

        access = app_session.get_access(code)
        token = Token(access['user_id'], access['access_token'], access['expires_in'])
        usr = User(token)
        session['vk_user_id'] = str(usr.vk_user_id)

        try:
            with app.app_context():
                db_session.query(Token).filter(Token.id == session['vk_user_id']).delete()
                db_session.commit()
        except NoResultFound:
            pass

        response = make_response(render_template('index.html'))

        with app.app_context():
            db_session.add(token)
            db_session.add(usr)
            db_session.commit()

        return response
    except VkException as e:
        return render_template('server_error.html', error_msg=e.message)


@app.route('/auth', methods=['GET'])
def auth():
    response = make_response(redirect(url_for('graph')))
    code = request.args.get('code')
    session['code'] = code

    return response


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/data')
def send_data():
    if 'vk_user_id' not in session:
        return make_response(redirect(url_for('login')))

    vk_user_id = str(session['vk_user_id'])
    with app.app_context():
        try:
            data = db_session.query(User).filter(User.vk_user_id == vk_user_id).one().graph
            return jsonify(json.loads(data))
        except NoResultFound as e:
            return make_response(redirect(url_for('login')))


if __name__ == '__main__':
    app.run(debug=True)

# TODO
# Настроить каскадное удаление объектов
