# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from bs4 import BeautifulSoup
import requests
import json

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        searchTerm = self.path[1:]
        result = self.get_google_img(searchTerm)
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(
            {"imgUrl": result[0], "searchUrl": result[1]}, indent=4), "utf-8"))

    def get_google_img(self, query):
        """
        gets a link to the first google image search result
        :param query: search query string
        :result: url string to first result
        """
        url = "https://www.google.com/search?q=" + \
            str(query) + "&source=lnms&tbm=isch"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

        html = requests.get(url, headers=headers).text

        soup = BeautifulSoup(html, 'html.parser')
        image = soup.find("img", {"class": "yWs4tf"})

        if not image:
            return ("notfound", "notfound")
        return (image['src'], url)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
