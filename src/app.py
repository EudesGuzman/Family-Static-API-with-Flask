import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members
    if response_body is None:
        return 'the server encounter an error', 500
    if members: 
        return jsonify(response_body), 200
    else: 
        return 'Family not found', 400

# -----------------------------------------------------------------------------------------------------------------
@app.route('/member/<int:id>', methods=['GET'])
def handle_get_single(id):
    member = jackson_family.get_member(id)
    print('@@@@@@@@@@@@@@@@@@@@@@@', member)
    if not member: 
        return {'Member not found': 404}
    else: 
        return jsonify(member)

@app.route('/member/<int:id>', methods=['DELETE'])
def handle_del_single(id):
    memberEliminate = jackson_family.get_member(id)
    member = jackson_family.delete_member(id)
    if not member:
        return 'Member not found', 400
    else:
        return jsonify({ "done" : True}), 200


@app.route('/member', methods=['POST'])
def handle_add_single():
    body = request.get_json()
    if body['first_name'] != '' and body['age'] != '' and body['lucky_numbers'] != '':
        if body['id'] == " ":
            body['id']=jackson_family._generateId()
        member = jackson_family.add_member(body)
        return jsonify({}), 200
    else: 
        return 'Incomplete member', 400 

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
