from app.modules.enums import VkApiErrors
from app.modules.vk_exception import VkException


class VkApiResponse:
    def __init__(self, response: dict):
        if VkApiErrors.ERROR.value in response.keys():
            raise VkException(str(response))

        self._response = response

    def __getitem__(self, key):
        return self._response[key]

