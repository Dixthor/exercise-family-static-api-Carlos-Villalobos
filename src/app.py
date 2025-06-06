import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure # Asegúrate de que FamilyStructure está importada

# from models import Person # Si no estás usando esto, puedes comentarlo o eliminarlo


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Crea el objeto de la familia Jackson
jackson_family = FamilyStructure("Jackson")


# Maneja/serializa errores como un objeto JSON
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Genera el sitemap con todos tus endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# Endpoint GET para obtener todos los miembros
@app.route('/members', methods=['GET'])
def get_family_members(): 
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# --- NUEVO ENDPOINT PARA AÑADIR MIEMBROS ---
@app.route('/members', methods=['POST']) 
def add_member():
 
    request_body = request.json
    print("Incoming request to add member with body:", request_body)
    new_member_data = {
        "first_name": request_body["first_name"],
        "age": request_body["age"],
        "lucky_numbers": request_body["lucky_numbers"]
    }
    if not 'id' in request_body:
        new_member_data['id'] = jackson_family._generate_id()
    else:
        new_member_data['id'] = request_body['id']
    
    jackson_family.add_member(new_member_data) 
    return jsonify(new_member_data), 200 

@app.route('/members/<int:id>', methods = ['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if not member:
        return jsonify('Member not found'), 400
    return jsonify(member), 200

@app.route('/members/<int:id>', methods = ['DELETE'])
def delete_member(id):
    result = jackson_family.delete_member(id)
    if not result:
        return jsonify({'done': result}), 400
    return jsonify({'done': result}), 200


# Esto solo se ejecuta si `$ python src/app.py` es ejecutado
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
