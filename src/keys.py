import context

from requests_oauthlib import OAuth1

from src.exceptions import APIKeyNotSet

class Keys:
    
    def set_api_key(self, key: str) -> None:
        """
        Sets API key.

        :param key: The API key from the TheNounProject API.
        :type key: str
        """
        self.api_key = key

    @property
    def api_key(self) -> str:
        """
        Getter for api_key property.

        :returns: The API key from the TheNounProject API.
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, key: str) -> None:
        """
        Setter for api_key property.

        :param key: The API key from the TheNounProject API.
        :type key: str
        """
        self._api_key = key
    
    def set_secret_key(self, secret: str) -> None:
        """
        Sets API secret.

        :param secret: The secret key from the TheNounProject API
        :type secret: str
        """
        self.secret_key = secret

    @property
    def secret_key(self) -> str:
        """
        Getter for secret_key property.

        :returns: The secret key from the TheNounProject API.
        :rtype: str
        """
        return self._secret_key
    
    @secret_key.setter
    def secret_key(self, secret: str) -> None:
        """
        Setter for secret_key property.

        :param secret: The secret key from the TheNounProject API.
        :type secret: str
        """
        self._secret_key = secret

    def _get_oauth(self) -> OAuth1:
        """
        Asserts that both api and secret keys have been set. 

        :raise AssertionError: Raises exception when api or secret keys have not been set.

        :returns: Returns an OAuth object using this object's API and secret key.
        :rtype: OAuth1
        """
        if not isinstance(self.api_key, str):
            raise APIKeyNotSet("api_key")
        if not isinstance(self.secret_key, str):
            raise APIKeyNotSet("secret_key")
        return OAuth1(self.api_key, self.secret_key)
