from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/googleff9deb20e4a46255.html')
def upload_file():
    return 'google-site-verification: googleff9deb20e4a46255.html'


if __name__ == '__main__':
    app.run(debug=True)