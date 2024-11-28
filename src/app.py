"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
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
def get_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as error: 
        return jsonify("Intentelo mas tarde"),500
    

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    try:
        member = jackson_family.get_member(id)
        if member is None:
            return jsonify("No existe este miembro"),404
        return jsonify(member),200

    except Exception as error:
        return jsonify("Intentelo mas tarde"),500
    

@app.route('/member', methods=["POST"])
def add_member():
    try:
        member = request.json
        if type(member) == dict:
            result = jackson_family.add_member(member)
            return jsonify(result),200
    except Exception as error:
        return jsonify("Intentelo mas tarde"),500
    
@app.route('/member/<int:member_id>', methods=["DELETE"])
def delete_member(member_id):
    dic = {"done":False}
    try:
        result=jackson_family.delete_member(member_id)
        if(result==True):
            dic["done"] = True
            return jsonify(dic),200
        return jsonify("No existe este miembro"),404
    except Exception as error:
        return jsonify("Intentelo mas tarde"),500
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
