from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import bcrypt
from marshmallow import Schema, fields, ValidationError
# object serialization/deserialization 
# (converting complex data types, such as objects, 
# to and from Python data types, like dictionaries)

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Connect to the MongoDB db
connection_url = app.config['DATABASE_URI']
client = MongoClient(connection_url)
db = client['user_db']
users_collection = db['users']

# users_collection.createIndex({ "email": 1 }, { "unique": True })

class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, )

# Helper function to convert ObjectId to string
# Else the bytes data creates problem when jsonify-ing
def serialize_user(user):
    user['_id'] = str(user['_id'])
    user['password'] = str(user['password'])
    return user

@app.route('/')
def home():
    return "Welcome to the website"

@app.route('/users', methods=['GET'])
def get_all_users():
    users = [serialize_user(user) for user in users_collection.find()]
    return jsonify(users)

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    if user:
        return jsonify(serialize_user(user))
    return jsonify({'message': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    try:
        print(request.json)
        data = UserSchema().load(request.json)
        data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        user_id = users_collection.insert_one(data).inserted_id
        return jsonify({'message': 'User created successfully', 'id': str(user_id)}), 201
    except ValidationError as e:
        return jsonify({'message': 'Invalid request data', 'errors': e.messages}), 400
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        print(request.json)
        data = UserSchema().load(request.json)
        result = users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': data})
        if result.modified_count > 0:
            return jsonify({'message': 'User updated successfully'})
        return jsonify({'message': 'User not found'}), 404
    except ValidationError as e:
        return jsonify({'message': 'Invalid request data', 'errors': e.messages}), 400

    except DuplicateKeyError: # Duplicate mail
        return jsonify({'message': 'User with this email already exists'}), 400

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = users_collection.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])
