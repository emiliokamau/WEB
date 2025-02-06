from flask import Flask, request, render_template_string, redirect, url_for, send_file
import csv
import os
from werkzeug.utils import secure_filename
from fpdf import FPDF

# Initialize Flask app
app = Flask(__name__)

# File for storing student data
DATA_FILE = "students.csv"
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Communities
COMMUNITIES = ["Cyber Security", "Web Development", "IoT (Internet of Things)", "DS/ML/AI"]

# HTML Templates
index_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Registration</title>
</head>
<body>
    <h1>Register a Student</h1>
    <form action="/register" method="post" enctype="multipart/form-data">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required><br><br>

        <label for="reg_no">Registration Number:</label>
        <input type="text" id="reg_no" name="reg_no" required><br><br>

        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br><br>

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br><br>

        <label for="community">Which community are you a member of?</label>
        <select id="community" name="community" required>
            {% for community in communities %}
            <option value="{{ community }}">{{ community }}</option>
            {% endfor %}
        </select><br><br>

        <label for="profile_picture">Profile Picture:</label>
        <input type="file" id="profile_picture" name="profile_picture" accept="image/*" required><br><br>

        <button type="submit">Register</button>
    </form>
    <a href="/list">View Registered Students</a>
</body>
</html>
"""

success_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Success</title>
</head>
<body>
    <h1>Student Registered Successfully!</h1>
    <p>Name: {{ name }}</p>
    <p>Registration Number: {{ reg_no }}</p>
    <p>Username: {{ username }}</p>
    <p>Community: {{ community }}</p>
    <img src="{{ profile_picture }}" alt="Profile Picture" width="150"><br><br>
    <a href="/">Go Back</a>
</body>
</html>
"""

list_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registered Students</title>
</head>
<body>
    <h1>Registered Students</h1>
    <table border="1">
        <tr>
            <th>Name</th>
            <th>Registration Number</th>
            <th>Username</th>
            <th>Community</th>
            <th>Profile Picture</th>
        </tr>
        {% for student in students %}
        <tr>
            <td>{{ student[0] }}</td>
            <td>{{ student[1] }}</td>
            <td>{{ student[2] }}</td>
            <td>{{ student[3] }}</td>
            <td><img src="{{ student[4] }}" alt="Profile Picture" width="50"></td>
        </tr>
        {% endfor %}
    </table>
    <a href="/">Go Back</a><br><br>
    <a href="/download">Download Student List</a>
</body>
</html>
"""

# Save data to file
def save_to_file(name, reg_no, username, password, community, profile_picture):
    with open(DATA_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, reg_no, username, password, community, profile_picture])

# Read data from file
def read_from_file():
    try:
        with open(DATA_FILE, mode="r") as file:
            reader = csv.reader(file)
            return list(reader)
    except FileNotFoundError:
        return []

@app.route('/')
def index():
    return render_template_string(index_template, communities=COMMUNITIES)

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    reg_no = request.form['reg_no']
    username = request.form['username']
    password = request.form['password']
    community = request.form['community']

    # Handle profile picture upload
    profile_picture = request.files['profile_picture']
    filename = secure_filename(profile_picture.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    profile_picture.save(filepath)

    # Save data to CSV
    save_to_file(name, reg_no, username, password, community, filepath)

    return render_template_string(success_template, name=name, reg_no=reg_no, username=username, community=community, profile_picture=filepath)

@app.route('/list')
def list_students():
    students = read_from_file()
    return render_template_string(list_template, students=students)

@app.route('/download')
def download():
    return send_file(DATA_FILE, as_attachment=True)

if __name__ == '__main__':
    try:
        from fpdf import FPDF
    except ImportError:
        raise ImportError("Please install fpdf using 'pip install fpdf' to proceed.")

    app.run(debug=True, use_reloader=False)
