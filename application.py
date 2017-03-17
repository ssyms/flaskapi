from flask import Flask, jsonify, request
from application import db
from application.models import User

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'

@application.route("/")
def hello():
    return "Hello World! Access a basic api."

def user_dict(user):
    user_dict = {
        "uid": str(user.uid),
        "firstName": str(user.firstName),
        "lastName": str(user.lastName),
        "dob": str(user.dob)
    }
    if user.dod is not None:
        user_dict["dod"] = str(user.dod)

    return user_dict

def error_msg(method, url, message):
    error_dict = {
        "verb": method,
        "url": url,
        "message": message
    }
    return error_dict

@application.route("/api/objects/<int:user_id>", methods=['GET'])
def get_object(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify(error_msg("GET", request.url, "Object does not exist."))
    return jsonify(user_dict(user))

@application.route("/api/objects", methods=['GET'])
def get_objects():
    users = User.query.all()
    user_arr = []
    for u in users:
        user_arr.append({"url": request.url + "/" + str(u.uid)})
    return jsonify({'objects': user_arr})

@application.route('/api/objects', methods=['POST'])
def create_object():
    if not request.json:
        return jsonify(error_msg("POST", request.url, "Not a JSON object."))
    if not ('firstName' in request.json and 'lastName' in request.json and 'dob' in request.json):
        return jsonify(error_msg("POST", request.url, "Does not include required fields."))

    first = request.json['firstName']
    last = request.json['lastName']
    dob = request.json['dob']
    new_user = User(firstName=first, lastName=last, dob=dob)
    if 'dod' in request.json:
        dod = request.json['dod']
        new_user.dod = dod

    db.session.add(new_user)
    db.session.commit()
    return jsonify(user_dict(new_user)), 201

@application.route('/api/objects/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    u = User.query.get(user_id)
    if not request.json:
        return jsonify(error_msg("PUT", request.url, "Not a JSON object."))
    if not ('firstName' in request.json and 'lastName' in request.json and 'dob' in request.json):
        return jsonify(error_msg("PUT", request.url, "Does not include required fields."))

    user = User.query.get(user_id)
    if user is not None:
        user.firstName = request.json['firstName']
        user.lastName = request.json['lastName']
        user.dob = request.json['dob']
        if 'dod' in request.json:
            user.dod = request.json['dod']
        db.session.commit()
        return jsonify(user_dict(user)), 201
    else:
        return jsonify(error_msg("PUT", request.url, "Object with given id does not exist."))

@application.route('/api/objects/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify(error_msg("DELETE", request.url, "Object does not exist."))
    db.session.delete(user)
    db.session.commit()
    return ('', 200)

if __name__ == "__main__":
    application.run()
