import db
from flask import Flask, jsonify, request, Response
from bson import json_util
from bson.objectid import ObjectId
import json



app = Flask(__name__)

# Select the database
# Select the collection

@app.route("/")
def get_initial_response():
    """Welcome message for the API."""
    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Si funka el api'
    }
    # Making the message looks good
    resp = jsonify(message)
    # Returning the object
    return resp


@app.route("/vacantes", methods=['POST'])
def create_vacante():
    
    idcarrera = request.json['idcarrera']
    idvacante = request.json['idvacante']
    cupo = request.json['cupo']
    requisitos = request.json['requisitos']

    if idcarrera and idvacante and cupo and requisitos:
        id = db.db.vacantes.insert_one({'idcarrera': idcarrera, 'idvacante': idvacante, 'cupo': cupo, 'requisitos': requisitos})
        response = jsonify({
            '_id': str(id),
            'idcarrera': idcarrera,
            'idvacante': idvacante,
            'cupo': cupo,
            'requisitos': requisitos
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route("/vacantes", methods=['GET'])
def fetch_vacantes():
    vacantes = db.db.vacantes.find()
    response = json_util.dumps(vacantes)
    return Response(response, mimetype="application/json")

@app.route("/vacantes/<id>", methods=['POST'])
def get_vacante(id):
    print(id)
    vacante = db.db.vacantes.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(vacante)
    return Response(response, mimetype="application/json")


@app.route("/vacantes/<id>", methods=['DELETE'])
def remove_vacante(id):
    db.db.vacantes.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Vacante' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

@app.route('/vacantes/<_id>', methods=['PUT'])
def update_vacante(_id):
    idcarrera = request.json['idcarrera']
    idvacante = request.json['idvacante']
    cupo = request.json['cupo']
    requisitos = request.json['requisitos']
    if idcarrera and idvacante and cupo and requisitos and _id:
        db.db.vacantes.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'idcarrera': idcarrera, 'idvacante': idvacante, 'cupo': cupo, 'requisitos': requisitos}})
        response = jsonify({'message': 'Vacante' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)
