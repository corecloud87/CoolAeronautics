from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
SECRET_KEY = 'your_secret_key'

devices = {"device1": "password123", "device2": "password456"}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    device_id = data.get('device_id')
    password = data.get('password')

    if devices.get(device_id) == password:
        token = jwt.encode({'device_id': device_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY)
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
