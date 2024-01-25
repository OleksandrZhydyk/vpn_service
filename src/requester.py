from requests import Session, adapters, Response
from urllib3 import Retry


class Requester(object):
    max_retry = 3
    retry_http_codes = (429, 500, 502, 503, 504)
    retry_interval = 0.3
    retry_methods = ("GET", "POST")

    def get_request(self, url: str) -> Response:
        session = self._get_session()
        response = session.get(url)
        response.raise_for_status()
        return response

    def post_request(self, url: str, body) -> Response:
        session = self._get_session()
        response = session.post(url, data=body)
        response.raise_for_status()
        return response

    def _get_session(self) -> Session:
        session = Session()
        retries = Retry(
            total=self.max_retry,
            backoff_factor=self.retry_interval,
            status_forcelist=self.retry_http_codes,
            allowed_methods=self.retry_methods,
        )
        session.mount("https://", adapters.HTTPAdapter(max_retries=retries))
        session.mount("http://", adapters.HTTPAdapter(max_retries=retries))
        return session
