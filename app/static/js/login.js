const oauth_uri = "https://oauth.vk.com/authorize?client_id=51395060&display=page&redirect_uri=https:" +
    "//vk-social-graph.herokuapp.com/auth&scope=friends,offline&response_type=code&v=5.131"

const login_btn = document.getElementsByClassName('login-btn')[0];


login_btn.addEventListener('click', () => {
    window.location = oauth_uri;
})



