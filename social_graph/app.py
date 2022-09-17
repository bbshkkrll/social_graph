from flask import Flask, render_template, request, url_for, session, make_response
from modules.vk_session import VkSession, VkException
from social_graph.modules.user_data import UserData

app = Flask(__name__)


@app.route("/graph")
def graph():
    render_template('force_diricted_graph.html')


@app.route('/auth', methods=['GET'])
def auth():
    vk_session = VkSession()
    code = request.args.get('code')
    token = vk_session.get_access_token(code)
    vk_session = VkSession(token=token)

    response = make_response(
        render_template('login.html', token=token, user_info=vk_session.get_info_about_current_user()))
    response.set_cookie('code', code)
    response.set_cookie('token', token)

    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['uid'])
        main_id = request.form['uid']
        vk_session = VkSession()
        try:

            user_info = UserData(main_id, *vk_session.prepare_data(main_id))
            user_info.initialize_friends()
            user_info.dump_data_to_json('./static/data/graph_data.json')
        except VkException as e:
            print(e.message, e.code)
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
