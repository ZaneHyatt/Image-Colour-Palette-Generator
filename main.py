from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from forms import UploadImg

WORKING_WIDTH = 600
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
img_path = ""

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
bootstrap = Bootstrap(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_colors(amount):
    global img_path
    img = Image.open(img_path)
    print(img)
    og_width = img.size[0]
    og_height = img.size[1]
    width_percentage = WORKING_WIDTH / og_width
    new_height = int(og_height * width_percentage)
    img = img.resize((WORKING_WIDTH, new_height))
    img_data = np.asarray(img)
    img_data = img_data.reshape(-1, 3)
    color_cluster = KMeans(n_clusters=amount)
    color_cluster.fit(img_data)
    colors = color_cluster.cluster_centers_.tolist()
    color_palette = []
    for rgb_list in colors:
        new_colors = [int(value) for value in rgb_list]
        color_palette.append(new_colors)
    return color_palette



@app.route("/", methods=['GET', 'POST'])
def home():
    global img_path
    path = ''
    colours = ''
    is_photo = False
    form = UploadImg()
    if form.validate_on_submit():
        is_photo = True
        img_path = form.file.data
        if img_path.filename == '':
            flash('Please select a file')
            return render_template("index.html", form=form, is_photo=False)
        if not allowed_file(img_path.filename):
            flash('The image has to be ".jpg" or ".jpeg" file')
            return render_template("index.html", form=form, is_photo=False)
        colours = process_colors(int(form.count.data))
        img = Image.open(img_path)
        img.save(f'static/{img_path.filename}')
        path = f'static/{img_path.filename}'
    return render_template("index.html", form=form, img_path=path, is_photo=is_photo, colours=colours)

if __name__ == "__main__":
    app.run(debug=True)