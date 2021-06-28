from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    f = ''
    if request.method == 'POST':
        f = request.files['googleff9deb20e4a46255.html']
        f.save('/var/www/googleff9deb20e4a46255.html')
    return f