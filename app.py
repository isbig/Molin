from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/googleff9deb20e4a46255.html')
def upload_file():
    return 'google-site-verification: googleff9deb20e4a46255.html'

@app.route("/", methods=['POST', 'GET'])
def callback():
    # get X-Line-Signature header value
    state = request.headers['X-Goog-Resource-State']
    print(state)
    uri = request.headers['X-Goog-Resource-URI']
    id = request.headers['X-Goog-Channel-ID']
    reid = request.headers['X-Goog-Resource-URI']
    print(uri)
    print(id)
    print(reid)
    return '200'

if __name__ == '__main__':
    app.run()
