from flask import Flask, request, jsonify
import pymongo
import certifi
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from werkzeug.security import generate_password_hash,check_password_hash
import traceback

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "key-secret"
jwt = JWTManager(app)

MONGO_URI = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(
    'mongodb://localhost:27017/',
    tlsCAFile=certifi.where()
)

db = client["test"]
collection = db["testing"]

@app.route("/test", methods = ["GET"])
def index():
    try:
        data = request.get_json()
        return jsonify(message="successfully created")
    except:
        print("Error")
        return 

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json.get
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return jsonify({"message": "Missing email or password"}), 400

        user = collection.find_one({"email":email})
        if user and check_password_hash(user["password"],password)
            access_token = create_access_token(identity={"email":email})
            return jsonify(token=access_token, name=user["name"], email=email), 200
    except Exception as e:
        print(f"error is {e} and {traceback.format_exc()}")
        return jsonify({"message":traceback.format_exc()})

@app.route("/register", methods=["POST"])
def register():
    try:
        data= request.get_json()
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")

        if not email or not password or not name:
            return jsonify({"message":"Missing name, password or email"}), 400
        if collection.find_one({"email": email}):
            return jsonify({"message":"Email aleady exists"}), 400

        hash_password = generate_password_hash(password)
        collection.insert_one({"email":email,"password": hash_password, "name": name})

        return jsonify({"message":"user register successfully"})

    except Exception as e:
        print(f"error{traceback.format_exc()}: {e}")
        return jsonify(message=traceback.format_exc())

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run(debug=True)
