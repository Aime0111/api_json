from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/")
def index():
    return "Hola Mundo"

# Definición del modelo de la tabla 'estudiantes'
class Alumno(db.Model):
    __tablename__ = 'alumnos'
    no_control = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    ap_paterno = db.Column(db.String)
    ap_materno = db.Column(db.String)
    semestre = db.Column(db.Integer)

    def to_dict(self):
        return {
            'no_control': self.no_control,
            'nombre': self.nombre,
            'ap_paterno': self.ap_paterno,
            'ap_materno': self.ap_materno,
            'semestre': self.semestre,
        }

# Endpoint para obtener todos los estudiantes
@app.route('/alumnos', methods=['GET'])
def listar_alumnos():
    alumnos = Alumno.query.all()
    listar_alumnos = []
    for alumno in alumnos:
        listar_alumnos.append({
            'no_control': alumno.no_control,
            'nombre': alumno.nombre,
            'ap_paterno': alumno.ap_paterno,
            'ap_materno': alumno.ap_materno,
            'semestre': alumno.semestre
        })
    return jsonify(listar_alumnos)

# Endpoint para agregar un nuevo estudiante
@app.route('/alumnos/new', methods=['POST'])
def agregar_alumno():
    data = request.get_json()
    nuevo_alumno = Alumno(
        no_control=data['no_control'],
        nombre=data['nombre'],
        ap_paterno=data['ap_paterno'],
        ap_materno=data['ap_materno'],
        semestre=data['semestre']
    )
    db.session.add(nuevo_alumno)
    db.session.commit()
    return jsonify({'mensaje': 'Alumno agregado exitosamente'}), 201

# Endpoint para actualizar un estudiante
@app.route('/alumnos/<no_control>', methods=['PUT'])
def actualizar_alumno(no_control):
    alumno = Alumno.query.get(no_control)
    if alumno is None:
        return jsonify({'mensaje': 'Alumno no encontrado'}), 404
    data = request.get_json()
    alumno.nombre = data['nombre']
    alumno.ap_paterno = data['ap_paterno']
    alumno.ap_materno = data['ap_materno']
    alumno.semestre = data['semestre']
    db.session.commit()
    return jsonify({'mensaje': 'Alumno actualizado exitosamente'})

# Endpoint para eliminar un estudiante
@app.route('/alumnos/<no_control>', methods=['DELETE'])
def eliminar_alumno(no_control):
    alumno = Alumno.query.get(no_control)
    if alumno is None:
        return jsonify({'mensaje': 'Alumno no encontrado'}), 404
    db.session.delete(alumno)
    db.session.commit()
    return jsonify({'mensaje': 'Alumno eliminado exitosamente'})

# Endpoint para obtener un estudiante por no_control
@app.route('/alumnos/<no_control>', methods=['GET'])
def obtener_alumno(no_control):
    alumno = Alumno.query.get(no_control)
    if alumno is None:
        return jsonify({'mensaje': 'Alumno no encontrado'}), 404
    return jsonify({
        'no_control': alumno.no_control,
        'nombre': alumno.nombre,
        'ap_paterno': alumno.ap_paterno,
        'ap_materno': alumno.ap_materno,
        'semestre': alumno.semestre
    })
