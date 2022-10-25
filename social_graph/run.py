from flask import request, render_template, make_response, redirect, url_for, jsonify

from app import app, app_session, db
from app.models import Token, User
from app.modules.vk_exception import VkException


@app.route("/graph")
def graph():
    try:
        if 'is_auth' in request.cookies.keys():
            return render_template('index.html')
    except Exception as e:
        print(e.args)
    try:
        code = request.cookies.get('code')
        access = app_session.get_access(code)
        token = Token(access['user_id'], access['access_token'], access['expires_in'])
        usr = User(token)

        graph = usr.get_graph()

        response = make_response(render_template('index.html'))
        response.set_cookie('usr_id', str(usr.user_id))
        response.set_cookie('is_auth', '1')
        db.session.add(token)
        db.session.add(usr)
        db.session.add(graph)
        db.session.commit()

        return response
    except VkException as e:
        return render_template('server_error.html', error_msg=e.message)


@app.route('/auth', methods=['GET'])
def auth():
    response = make_response(redirect(url_for('graph')))
    code = request.args.get('code')
    response.set_cookie('code', code)

    return response


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/data')
def send_data():
    data = User.query.get(vk_usr_id=f'{request.cookies.get("usr_id")}').graph.data
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
