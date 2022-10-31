class VkException(Exception):
    def __init__(self, err_message):
        self.message = err_message
