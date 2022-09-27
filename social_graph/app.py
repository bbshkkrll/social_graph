from flask import Flask, render_template, request, url_for, session, make_response, redirect
from modules.vk_session import VkSession
from social_graph.modules.user import User
from social_graph.modules.vk_exception import VkException

app = Flask(__name__)

app_session = VkSession()

users = {}


@app.route("/graph")
def graph():
    code = request.cookies.get('code')

    try:
        access = app_session.get_access(code)
        usr = User(access['expires_in'], access['user_id'], access['access_token'])
        usr.save_graph()

        return render_template('index.html')
    except VkException as e:
        render_template('server_error.html', error_msg=e.message)


@app.route('/auth', methods=['GET'])
def auth():
    response = make_response(redirect(url_for('graph')))
    code = request.args.get('code')
    response.set_cookie('code', code)

    return response


@app.route('/')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)

# TODO
# Front:
# 1. Statistic about friends vk
# Back:
# 1. Class for auth user
# 2. Hold user's token on server
# 3. Counting token's expired time
