from flask import Flask, render_template, request
from modules.vk_session import VkSession, VkException
from social_graph.modules.user_data import UserData

app = Flask(__name__)


@app.route("/graph")
def graph():
    return render_template('force_diricted_graph.html')


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
