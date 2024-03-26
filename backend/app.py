from flask import Flask, request, jsonify, session, send_file
import re
from flask.sessions import SecureCookieSessionInterface
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import uuid
import functools

## NEW IMPORTS
from transformers import pipeline
classifier = pipeline("image-classification", model="Devarshi/Brain_Tumor_Classification")
import json
from flask_cors import CORS, cross_origin
import bcrypt
from PIL import Image
from datetime import datetime
import io
from base64 import encodebytes
## END OF NEW IMPORTS

uri = "mongodb+srv://ishanupadhyayiitb:9nkF9l4e2C5RssD8@cluster0.yjw3qmt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
# Send a ping to confirm a successful connection

try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# MongoDB Atlas connection setup
uri = "mongodb+srv://ishanupadhyayiitb:9nkF9l4e2C5RssD8@cluster0.yjw3qmt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi("1"))
db = client.get_database("geeklogin")  # Assuming 'geeklogin' is your database name
users = db.accounts
projects = db.projects

print("Connected to MongoDB Atlas")

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = "ishan121028"

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        username = request.headers.get("username")
        token = request.headers.get("Authorization")
        
        if not token or not username:
            return jsonify(message="Missing token"), 201
        
        account = users.find_one({"username": username})
        if not account:
            return jsonify(message="User not found"), 201
        pwd = account.get("password")

        if not bcrypt.checkpw(pwd.encode('utf-8'), token[2:-1].encode('utf-8')):
            return jsonify(message="Invalid token"), 201

        return f(*args, **kwargs)

    return decorated_function

@app.route("/login", methods=["POST"])
def login():
    if request.method == "OPTIONS": # CORS preflight
        print("PREFLIGHT")
        return _build_cors_preflight_response(), 200

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username and password:
        account = users.find_one({"username": username, "password": password})
        if account:
            token = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            response = jsonify(
                message="Logged in successfully!",
                username=username,
                token=str(token),
            )
            return response, 200
        else:
            response = jsonify(message="Incorrect username/password!")
            return response, 401
    response = jsonify(message="Username and password are required!")
    return response, 400


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify(message="Logged out successfully!")


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()  # Get JSON data from the request
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    if username and password and email:
        if users.find_one({"username": username}):
            return jsonify(message="Account already exists!"), 409
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify(message="Invalid email address!"), 400
        elif not re.match(r"[A-Za-z0-9]+", username):
            return (
                jsonify(message="Username must contain only characters and numbers!"),
                400,
            )
        else:
            users.insert_one(
                {"username": username, "password": password, "email": email}
            )
            return jsonify(message="You have successfully registered!"), 200
    return jsonify(message="Please fill out the form!"), 400


@app.route("/create-project", methods=["POST"])
@login_required
def create_project():
    data = request.get_json()
    username = request.headers.get("username")
    project_name = data.get("project_name")

    if not project_name:
        return jsonify(message="Project name is required!"), 200
    
    # Assuming you have a 'projects' collection in your MongoDB database

    # Check if the project already exists
    if projects.find_one({"project_name": project_name, "username": username}):
        return jsonify(message="Project already exists!"), 200

    # Generate a unique token for the new project
    project_token = str(uuid.uuid4())
    while True:
        if not projects.find_one({"project_token": project_token}):
            break
        project_token = str(uuid.uuid4())

    # Insert the new project into the database
    projects.insert_one(
        {
            "username": username,
            "project_name": project_name,
            "project_token": project_token,
            "history": []
        }
    )

    return jsonify(message="Project created successfully!", project_token=project_token), 200

@app.route("/predict", methods=["POST"])
@login_required
def predict():
    username = request.headers.get("username")
    projectToken = request.headers.get("projectToken")

    image = request.files['image']
    print(image)
    pil_image = Image.open(image)
    out_format = '%Y_%m_%d_%H_%M_%S.%fZ'
    filename = f"images/{username}_{projectToken}_{str(datetime.now().strftime(out_format))}.jpg"
    pil_image.save(filename)

    scores = classifier(pil_image)
    toplabel = scores[0]['label']

    proj = projects.find_one({"project_token": projectToken, "username": username})
    print(proj)
    proj['history'].append({'image':filename, 'label':toplabel})
    print(proj)

    projects.update_one({"project_token": projectToken, "username": username}, {"$set": proj})

    return jsonify(prediction=toplabel, filename=filename), 200

@app.route('/images/<filename>',methods = ['GET'])
def getFile(filename):
    return send_file('images/' + filename)

@app.route("/", methods=["GET"])
@login_required
def home():

    def projects_required(l):
        newl = []
        for i in l:
            histnew = []
            hist = i["history"]
            for his in hist:
                histnew.append({'image':his['image'], 'label': his["label"]})

            newl.append({"project_name": i["project_name"], "project_token": i["project_token"], "history": histnew})
        print("newl", newl)
        return newl
    
    # Fetch user's project history based on username
    username = request.headers.get("username")
    user_projects = list(projects.find({"username": username}))
    return jsonify(user_projects=projects_required(user_projects)), 200

if __name__ == "__main__":
    app.run(debug=True)
