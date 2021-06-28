from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/googleff9deb20e4a46255.html')
def upload_file():
    return 'google-site-verification: googleff9deb20e4a46255.html'

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Goog-Resource-State']
    body = request.get_data(as_text=True)
    print(signature)
    print(body)



if __name__ == '__main__':
    app.run()
