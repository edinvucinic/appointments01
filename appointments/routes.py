from appointments import app
from flask import jsonify, request, session
from appointments.models import Patient, User


@app.route('/')
@app.route("/home")
def home():
    if not 'username' in session:
        resp = jsonify({'message': 'Unauthorized'})
        resp.status_code = 401
        return resp
    else:
        username = session['username']
        loggeduser = User.query.filter_by(username=username).first()
        patientsForUser=Patient.query.filter_by(owner=loggeduser.id)
        return jsonify({'patients': patientsForUser})


@app.route('/login', methods=['POST'])
def login():
    _json = request.json
    _username = _json['username']
    _password = _json['password']

    # validate the received values
    if _username and _password:
        attempted_user = User.query.filter_by(username=_username).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=_password
        ):
            return jsonify({'message': 'You are logged in successfully'})
    else:
        resp = jsonify({'message': 'Bad Request - invalid credendtials'})
        resp.status_code = 400
        return resp


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return jsonify({'message': 'You successfully logged out'})
