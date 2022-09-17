from flask import Flask, render_template, request, url_for, session, make_response
from modules.vk_session import VkSession, VkException
from social_graph.modules.user_data import UserData

app = Flask(__name__)


@app.route("/graph")
def graph():
    code = request.cookies.get('code')
    vk_session = VkSession()
    token = vk_session.get_access_token(code)
    vk_session = VkSession(token=token)
    try:
        user_info = UserData(vk_session.get_current_user_id(), *vk_session.prepare_data())
        user_info.initialize_friends()
        user_info.dump_data_to_json('./static/data/graph_data.json')
    except VkException as e:
        print(e.message, e.code)

    return render_template('force_diricted_graph.html')


@app.route('/auth', methods=['GET'])
def auth():
    code = request.args.get('code')

    response = make_response(
        render_template('login.html'))
    response.set_cookie('code', code)

    return response


@app.route('/')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
