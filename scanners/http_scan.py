import http.client
import requests


class HTTPScanner:
    def __init__(self, website):
        self.website = website
        self.http_server = None
        self.insecure_http = True
        self.redirect_to_https = False
        self.hsts = False

    def get_http_scan(self):
        response = self.get_response("http://" + self.website, 10)

        return self.http_server, self.insecure_http, self.redirect_to_https, self.hsts
        # connection = http.client.HTTPConnection(ip, port=80, timeout=2)
        # connection.request("GET", "/")
        # response = connection.getresponse()
        # server = response.headers["Server"]
        # print(response.getheaders())

        # return server, 'hi'

    def get_response(self, url, redirects_remaining):
        try:
            response = requests.get(url, timeout=2)
            # print(response.status_code)
            # print(response.url)
            # print(response.headers)
            # print(redirects_remaining)

            if 300 <= response.status_code and response.status_code <= 309:
                if redirects_remaining > 0:
                    self.get_response(response.url, redirects_remaining - 1)

            if redirects_remaining > 0 and response.url.startswith("https://"):
                self.redirect_to_https = True

            if redirects_remaining > 0 and response.headers.get("Strict-Transport-Security"):
                self.hsts = True

            self.http_server = response.headers.get("Server")

        except Exception as ex:
            self.insecure_http = False



