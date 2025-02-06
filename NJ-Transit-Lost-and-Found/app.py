import os
from flask import Flask, render_template, request, redirect, url_for, flash
#from firebase_admin import credentials, firestore, storage
#from firebase import upload_item, search_items
from werkzeug.utils import secure_filename
import jsonify
from ai import *
import mimetypes

import subprocess
from PIL import Image
import pyheif


# Ensure the upload folder exists

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.secret_key = 'flask-app'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_heic_to_jpg(heic_file_path, jpg_file_path):
    """Convert HEIC file to JPG format using ImageMagick."""
    try:
        command = ['magick', 'convert', heic_file_path, jpg_file_path]
        subprocess.run(command, check=True)
        return jpg_file_path
    except subprocess.CalledProcessError as e:
        print(f"Error converting HEIC to JPG: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        return render_template('sign-in.html')
    else:
        employee_id = request.form.get('employee-id')
        password = request.form.get('password')
        print(employee_id, password)
        if employee_id == '123456789' and password == 'user':
            return redirect(url_for('homepage'))
        else:
            flash('Wrong employee id or password')
            return redirect(url_for('sign_in'))
        
@app.route('/employee-portal', methods=['GET'])
def employee_portal():
    return render_template('employee.html')

@app.route('/report_claim', methods=['GET'])
def report_claim():
    return render_template('report-claim.html')

@app.route('/home-page',methods=['GET'])
def homepage():
    return render_template('home-page.html')


@app.route('/lost_item',methods=['GET', 'POST'])
def lost_item():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        category = request.form.get('category')
        busRoute = request.form.get('bus_route')
        busStation = request.form.get('bus_station')
        trainStation = request.form.get('train_station')
        trainLine = request.form.get('train_line')
        return redirect(url_for('submit_item'))
    return render_template('lost-item.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        category = request.form.get('category')
        description = request.form.get('description')
        bus_route = request.form.get('bus_route')
        bus_stop = request.form.get('bus_stop')
        train_station = request.form.get('train_station')
        train_line = request.form.get('train_line')

        # Handle the uploaded image
        image_data = request.form.get('image')

        try:
            # Decode the base64 image and save it temporarily
            filename = "uploaded_image.jpg"  # You can generate a dynamic name if needed
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))

            # Remove the prefix if present (e.g., "data:image/jpeg;base64,...")
            if ',' in image_data:
                image_data = image_data.split(',')[1]

            with open(file_path, 'wb') as img_file:
                img_file.write(base64.b64decode(image_data))

            # Determine category based on bus/train data
            dynamic_category = 'Bus Stop' if bus_route or bus_stop else 'Train Station'

            # Call the upload_item function
            upload_item(
                image_path=file_path,
                category=category or dynamic_category,
                description=description,
                bus_route=bus_route,
                bus_stop=bus_stop,
                train_line=train_line,
                train_station=train_station
            )

            return redirect(url_for('search_results'))  # Redirect to a success page
        except Exception as e:
            return redirect(url_for('search_results'))
    return redirect(url_for('search_results'))

@app.route('/search_results',methods=['GET'])
def search_results():
    items = search_items('Bus Stop', '814', 'Cell Phones')
    return render_template('search-results.html', items=items)


@app.route('/claim',methods=['GET'])
def claim():
    return render_template('claim.html')

@app.route('/submit_item', methods=['GET', 'POST'])
def submit_item():
    return render_template('confirm.html')




if __name__ == '__main__':
    app.run(debug=True)
