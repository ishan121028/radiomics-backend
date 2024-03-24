from flask import Flask, request, jsonify, session
import re
from flask.sessions import SecureCookieSessionInterface
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import uuid
import functools

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
app.secret_key = "ishan121028"


def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return jsonify(message="Not logged in!"), 403
        return f(*args, **kwargs)

    return decorated_function


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username and password:
        account = users.find_one({"username": username, "password": password})
        if account:
            session_serializer = SecureCookieSessionInterface().get_signing_serializer(
                app
            )
            session_token = session_serializer.dumps({"username": username})
            session["loggedin"] = True
            session["username"] = username
            return jsonify(
                message="Logged in successfully!",
                username=username,
                token=session_token,
            )
        else:
            return jsonify(message="Incorrect username/password!"), 401
    return jsonify(message="Username and password are required!"), 400


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
            return jsonify(message="You have successfully registered!")
    return jsonify(message="Please fill out the form!"), 400


@app.route("/create-project", methods=["POST"])
def create_project():
    data = request.get_json()
    project_name = data.get("project_name")
    model_name = data.get("model_name")

    if not project_name or not model_name:
        return jsonify(message="Project name and model name are required!"), 400

    # Generate a unique token for the new project
    project_token = str(uuid.uuid4())

    # Assuming you have a 'projects' collection in your MongoDB database

    # Check if the project already exists
    if projects.find_one({"project_name": project_name}):
        return jsonify(message="Project already exists!"), 400

    # Insert the new project into the database
    projects.insert_one(
        {
            "project_name": project_name,
            "model_name": model_name,
            "project_token": project_token,
        }
    )

    return jsonify(message="Project created successfully!", project_token=project_token)


@app.route("/", methods=["GET"])
@login_required
def home():
    username = session.get("username")
    # Fetch user's project history based on username
    user_projects = list(projects.find({"username": username}, {"_id": 0}))
    return jsonify(user_projects=user_projects)


if __name__ == "__main__":
    app.run(debug=True)
