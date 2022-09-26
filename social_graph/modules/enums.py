from enum import Enum


class VkApiMethods(Enum):
    FRIENDS_GET = 'friends.get'
    USERS_GET = 'users.get'
    FRIENDS_GET_MUTUAL = 'friends.getMutual'
    EXECUTE_GET_MUTUAL_FRIENDS = 'execute.get_mutual_friends'
    AUTHORIZE = 'authorize'
    ACCESS_TOKEN = 'access_token'
    METHOD_URL = 'https://api.vk.com/method/'
    OUAUTH_URL = 'https://oauth.vk.com/'


class VkApiFields(Enum):
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    FRIENDS = 'friends'
    PHOTO = 'photo'
    PAGE = 'page'
    CODE = 'code'
    UID = 'uid'
    SEX = 'sex'
    ID = 'id'


class VkApiKeys(Enum):
    DISPLAY = 'display'
    USER_ID = 'user_id'
    USER_IDS = 'user_ids'
    CLIENT_ID = 'client_id'
    CLIENT_SECRET = 'client_secret'
    REDIRECT_URI = 'redirect_uri'
    CODE = 'code'
    SCOPE = 'scope'
    RESPONSE_TYPE = 'response_type'
    FIELDS = 'fields'
    ACCESS_TOKEN = 'access_token'
    V = 'v'


class VkApiError(Enum):
    ERROR = 'error'
    ERROR_CODE = 'error_code'
    ERROR_MSG = 'error_msg'
    ERROR_DSCPN = 'error_description'
