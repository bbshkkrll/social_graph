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

        filename = usr.save_graph()
        filename_json = '.' + filename

        response = make_response(render_template('index.html'))
        response.set_cookie('filename_json', filename_json)
        response.set_cookie('usr_id', access['user_id'])
        users[access['user_id']] = usr

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


if __name__ == '__main__':
    app.run(debug=True)

# TODO
# Front:
# 1. Statistic about friends vk
# Back:
# 1. Class for auth user DONE
# 2. Hold user's token on server
