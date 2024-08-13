import base64
from typing import Optional
from proxy.http.proxy import HttpProxyBasePlugin
from proxy.http.parser import HttpParser
from proxy.http.exception import ProxyAuthenticationFailed

class MultiUserAuthPlugin(HttpProxyBasePlugin):

    """Придумать где внешне хранить креды. И как их динамично тут обновлять при добавлени\изменении. Либо ребутить проксю"""

    USERS = {
        'user1': 'password1',
        'user2': 'password2',
    }

    def before_upstream_connection(
        self, request: HttpParser
    ) -> Optional[HttpParser]:
        print(request.__dict__)
        if not self.is_authenticated(request):
            raise ProxyAuthenticationFailed()
        return request

    def handle_client_request(
        self, request: HttpParser
    ) -> Optional[HttpParser]:
        return request

    def on_client_data(
        self, raw: memoryview
    ) -> Optional[memoryview]:
        return raw

    def is_authenticated(self, request: HttpParser) -> bool:
        auth_header = request.headers.get(b'proxy-authorization')
        if auth_header:
            try:
                auth_type, credentials = auth_header[1].split(b' ', 1)
                if auth_type.lower() == b'basic':
                    decoded_credentials = base64.b64decode(credentials).decode('utf-8')
                    username, password = decoded_credentials.split(':', 1)
                    if self.USERS.get(username) == password:
                        return True
            except Exception as e:
                print(f"Ошибка в процессе авторизации: {e}")
        return False
        
