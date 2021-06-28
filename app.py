from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/googleff9deb20e4a46255.html')
def upload_file():
    return 'google-site-verification: googleff9deb20e4a46255.html'

@app.route("/", methods=['POST', 'GET'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Goog-Resource-State', 'X-Goog-Resource-URI', 'X-Goog-Channel-ID']
    print(signature)
    return '200'

if __name__ == '__main__':
    app.run()
