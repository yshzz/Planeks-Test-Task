import requests
from envparse import env
from validators import url as url_validator
from .exceptions import MailgunError
import json

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'
DEFAULT_BASE_URL = 'https://api.mailgun.net'


class Api:
    """
        Base class for API interaction.

        Args:
            key (:obj:`str`): API key.
            endpoint (:obj:`str`): API base url.
    """

    def __init__(self, key=None, endpoint=DEFAULT_BASE_URL):
        self.key = key or env('MAILGUN_API_KEY')
        self.endpoint = endpoint

    def _perform_request(self, url, method='GET', params=None):
        url = self._get_formed_url(url)

        if params is None:
            params = {}

        # Lookup table to find out the appropriate requests method and payload type.
        lookup = {
            GET: (requests.get, 'params'),
            POST: (requests.post, 'data'),
            PUT: (requests.put, 'data'),
            DELETE: (requests.delete, 'params')
        }

        requests_method, payload = lookup[method]
        kwargs = {payload: params, 'auth': ('api', self.key)}
        print(requests_method)
        print(kwargs)
        print(url)

        return requests_method(url, **kwargs)

    def get_data(self, url, method='GET', params=None):
        """
            Process HTTP response.

            Use this method everytime you need to make API request.

            Args:
                url (:obj:`str`): Path where to execute request.
                method (:obj:`str`, optional): HTTP request method.
                params (:obj:`dict`, optional): HTTP request params.

            Returns:
                :obj:`dict`: Response data.

            Raises:
                :class:`mailgun.MailgunError`: Mailgun error.
        """

        response = self._perform_request(url, method, params)
        data = response.json()
        print(data)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            error_message = data.get('message')
            raise MailgunError(error_message)

        print("s")

        return data

    def _get_formed_url(self, url):
        # Typical case for url forming.
        typical_case = self.endpoint + url

        if self.endpoint.endswith('/'):
            formed_url = typical_case if not url.startswith('/') else self.endpoint[:-1] + url
        else:
            formed_url = typical_case if url.startswith('/') else self.endpoint + '/' + url

        if url_validator(formed_url):
            return formed_url
        else:
            raise ValueError(f'Url "{formed_url}" is not valid!')


class Mailgun(Api):
    """
        Mailgun client.

        Args:
            key (:obj:`str`): API key.
            endpoint (:obj:`str`): API base url.
            domain (:obj:`str`): Mailgun domain to use.
    """

    def __init__(self, key=None, endpoint=DEFAULT_BASE_URL, domain=None):
        super().__init__(key, endpoint)
        self.domain = domain or env('MAILGUN_DOMAIN')

    def send_email(self, to, subject, text, **kwargs):
        params = {
            'from': f'noreply@{self.domain}',
            'to': to,
            'subject': subject,
            'text': text
        }
        params.update(kwargs)

        return self.get_data(
            f'/v3/{self.domain}/messages',
            method=POST,
            params=params
        )

    def validate_email(self, email):
        params = {'address': email}
        return self.get_data('/v4/address/validate', method=GET, params=params)
