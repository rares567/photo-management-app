from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
import os
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
app.secret_key = 'HateForAssembly'

ALLOWED_FORMATS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_LOCATION'] = 'static/uploads/'
app.config['THUMBNAIL_LOCATION'] = 'static/thumbnails/'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'secret'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FORMATS

@app.route('/')
def index():
    categories = os.listdir(app.config['UPLOAD_LOCATION'])
    photos = {category: os.listdir(os.path.join(app.config['UPLOAD_LOCATION'], category)) for category in categories}
    return render_template('index.html', photos=photos)

@app.route('/about_me')
def about_me():
    return render_template('about_me.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['logged_in'] = True
    return redirect(url_for('index'))

@app.route('/signout')
def signout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

def create_thumbnail(image_path, thumbnail_path):
    with Image.open(image_path) as img:
        img.thumbnail((200, 200))
        img.save(thumbnail_path)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    name = request.form['rename']
    category = request.form['category']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if name:
            filename = f"{secure_filename(name)}.{filename.rsplit('.', 1)[1]}"
        category_path = os.path.join(app.config['UPLOAD_LOCATION'], category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
        file_path = os.path.join(category_path, filename)
        file.save(file_path)

        thumbnail_path = os.path.join(app.config['THUMBNAIL_LOCATION'], category)
        if not os.path.exists(thumbnail_path):
            os.makedirs(thumbnail_path)
        thumbnail_file_path = os.path.join(thumbnail_path, f"{filename.rsplit('.', 1)[0]}.thumb.{filename.rsplit('.', 1)[1]}")
        create_thumbnail(file_path, thumbnail_file_path)     
    return redirect(url_for('index'))

@app.route('/uploads/<category>/<filename>')
def uploaded_file(category, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_LOCATION'], category), filename)

@app.route('/thumbnails/<category>/<filename>')
def thumbnail_file(category, filename):
    return send_from_directory(os.path.join(app.config['THUMBNAIL_LOCATION'], category), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
