import os
#import magic
import urllib.request
from app import app
from app import login_manager
from flask import Flask, Response, flash, request, redirect, render_template
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from models.user import User

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

# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == username + "_secret":
            id = username.split('user')[1]
            user = User(id)
            login_user(user)
            return redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
