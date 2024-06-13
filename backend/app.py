from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

def generate_token(user_id):
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return token

@app.route('/login', methods=['POST'])
def login():
    auth_data = request.get_json()
    user_id = auth_data.get('user_id')
    password = auth_data.get('password')

    if user_id == 'example_user' and password == 'password123':  # Example user validation
        token = generate_token(user_id)
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Token is missing'}), 403

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': f'Welcome user {data["user_id"]}!'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 403

@app.route('/data', methods=['GET'])
def get_data():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Token is missing'}), 403

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        sample_data = {
            'user_id': data['user_id'],
            'data': 'This is some protected data.'
        }
        return jsonify(sample_data)
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 403

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True, port = 5001)
