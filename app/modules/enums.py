from enum import Enum


class VkApiMethods(Enum):
    EXECUTE_GET_MUTUAL_FRIENDS = 'execute.get_mutual_friends'
    METHOD_URL = 'https://api.vk.com/method/'
    FRIENDS_GET_MUTUAL = 'friends.getMutual'
    OUAUTH_URL = 'https://oauth.vk.com/'
    ACCESS_TOKEN = 'access_token'
    FRIENDS_GET = 'friends.get'
    USERS_GET = 'users.get'
    AUTHORIZE = 'authorize'


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
    CLIENT_SECRET = 'client_secret'
    RESPONSE_TYPE = 'response_type'
    REDIRECT_URI = 'redirect_uri'
    ACCESS_TOKEN = 'access_token'
    TARGET_UIDS = 'target_uids'
    CLIENT_ID = 'client_id'
    USER_IDS = 'user_ids'
    DISPLAY = 'display'
    USER_ID = 'user_id'
    FIELDS = 'fields'
    SCOPE = 'scope'
    CODE = 'code'
    V = 'v'


class VkApiErrors(Enum):
    ERROR_DSCPN = 'error_description'
    ERROR_CODE = 'error_code'
    ERROR_MSG = 'error_msg'
    ERROR = 'error'
