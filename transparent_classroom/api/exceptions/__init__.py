class EntrypointNotFoundException(Exception):
    """
    Entrypoint Not Found Exception Class

    Attributes:


    """

    def __init__(self, model_name: str, behavior: str) -> None:
        """
        Entrypoint Not Found Exception Constructor

        :param model_name: str, The name of the model that was not
            found in the API.
        :param behavior: str, The expected behavior of the endpoint.
        :return: None

        """

        super().__init__(f"`{behavior}: {model_name}` Entrypoint Not Found in API.")
