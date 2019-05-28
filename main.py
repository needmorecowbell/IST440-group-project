import os
#import magic
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		f = request.files['file']
		if f.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if f and allowed_file(f.filename):
			filename = secure_filename(f.filename)

                        # when user login is added, the upload folder will make a directory
                        # named after the user, then all uploads from that user go into the
                        # folder.

			f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File(s) successfully uploaded')
			return redirect('/')

@app.route('/reports')
def get_reports():
    reports =  ["test report data 1","test report data 2"]
    # eventually this will be a list of the reports that a user has requested. 
    # the reports will be separated in a similar fashion to how the file upload works. 
    return render_template('reports.html', data=reports)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
