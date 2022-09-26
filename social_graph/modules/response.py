from social_graph.modules.enums import VkApiError


class VkApiResponse:
    def __init__(self, response: dict):
        if VkApiError.ERROR.value in response.keys():
            raise

        self._response = response['response']

    def __getitem__(self, key):
        return self._response[key]

