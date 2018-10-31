from flask import Flask, request
from flask_restful import Resource, Api
from hashids import Hashids
import re

hashids = Hashids()

app = Flask(__name__)
api = Api(app)

urls = {}
id = 0

class Url(Resource):
    def get(self, url_hash):
        s = str(request)
        extracted_text = re.search('''(?<=')\s*[^']+?\s*(?=')''', s)
        url = extracted_text.group().strip()
        if(urls.get("short") == url):
            return {'id': urls["id"], 'short': urls["short"], 'url': urls["url"]}, 200
        else:
            return "NOT FOUND", 404

    def delete(self, url_hash):
        s = str(request)
        extracted_text = re.search('''(?<=')\s*[^']+?\s*(?=')''', s)
        url = extracted_text.group().strip()
        if(urls.get("short") == url):
            urls.clear()
        return None, 204

class ShortenUrl(Resource):
    def post(self):
        global id
        url = request.values.get('url')
        if(urls.get("url") == url):
            return "Url already present!", 409
        else:
            id = id+1
            hashid = hashids.encode(id)
            urls["id"] = str(id)
            urls["short"] = "http://localhost:5000/url/"+hashid
            urls["url"] = url
        return {'id': urls["id"], 'short': urls["short"], 'url': urls["url"]}, 200


api.add_resource(ShortenUrl, '/url')
api.add_resource(Url, '/url/<string:url_hash>')

if __name__ == '__main__':
    app.run(debug=True)