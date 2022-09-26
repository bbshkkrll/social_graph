from flask import Flask, render_template, request, url_for, session, make_response, redirect
from modules.vk_session import VkSession
from social_graph.modules.user_data import UserData
from social_graph.modules.vk_exception import VkException

app = Flask(__name__)


@app.route("/graph")
def graph():
    code = request.cookies.get('code')

    render_template('code.html', code=code)

    # try:
    #     vk_session = VkSession()
    #     token = vk_session.get_access_token(code)
    #     vk_session = VkSession(token=token)
    #     user_info = UserData(vk_session.get_current_user_id(), *vk_session.prepare_data())
    #     user_info.initialize_friends()
    #     user_info.dump_data_to_json('./static/data/graph_data.json')
    # except VkException as e:
    #     return render_template('server_error.html', error_msg=e.message)
    #
    # return render_template('index.html')


@app.route('/auth', methods=['GET'])
def auth():
    code = request.args.get('code')

    response = make_response()
    response.set_cookie('code', code)
    # example
    # {
    #     "access_token": "533bacf01e11f55b536a565b57531ac114461ae8736d6506a3",
    #     "expires_in": 43200,
    #     "user_id": 66748
    # }

    return redirect(url_for('graph'), 200, response)


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
