import json
from flask import Flask, request
from usermodel import db, User


db_filename = 'auth.db'
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_filename}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

#cached variables:
_secret = 'DKNDKNASKVJNVJNFVJF'
_logged_in = []


db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return json.dumps({'success':True, 'data':data}), code

def failure_response(error, code=404):
    return json.dumps({'success':False, 'error':error}), code


def get_user_by_email(email):
    return User.query.filter(User.email == email ).first()

def get_user_by_session_token(token):
    return User.query.filter(User.session_token == token).first()

def get_user_by_refresh_token(token):
    return User.query.filter(User.refresh_token == token).first()

def extract_token(request):
    '''tokens are passed thru the 'Authorization' header using the bearer token scheme'''
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return False, 'Missing Authorization header'
    bearer_token = auth_header.split()[1]
    return True, bearer_token



@app.route('/register/', methods=['POST'])
def register_account():
    body = json.loads(request.data) #contains sent credentials
    email = body.get('email')
    password = body.get('password')
    if not email or not password:
        return failure_response('Either username or password missing')
    if get_user_by_email(email):
        return failure_response('User already exists')
    new_user = User(email=email, password=password) #password hashing and tokens generation handled by constructor
    db.session.add(new_user)
    db.session.commit()
    return success_response({
                            'user_email': new_user.email, 
                            'user_password':f'{password[0]}{'*'*(len(password)-1)}'
                            })


@app.route('/login/', methods=['POST'])
def login():
    body = json.loads(request.data) #contains sent credentials
    email = body.get('email')
    password = body.get('password')
    if not email or not password:
        return failure_response('Either username or password missing')
    user = get_user_by_email(email)
    if not user:
        return failure_response('Entered incorrect email Or user not yet registered')
    if not user.verify_password(password):
        return failure_response('Entered incorrect password')
    if not user.email in _logged_in:
        _logged_in.append(user.email)
    return success_response({
                             'session_token': user.session_token,
                             'session_expiration': str(user.session_expiration),
                             'refresh_token': user.refresh_token
                              })


@app.route('/session/')
def update_session():
    '''handles refresh tokens'''
    success, resp  = extract_token(request)
    if not success:
        return failure_response(resp)
    else:
        refresh_token = resp
    user = get_user_by_refresh_token(refresh_token)
    if not user:
        return failure_response('Invalid refresh token')
    if not user.email in _logged_in:
        return failure_response('User not logged in; please log in')
    user.renew_session() #regenerate token fields (refresh token also regenerated)
    db.session.commit()
    return success_response({
                             'session_token': user.session_token,
                             'session_expiration': str(user.session_expiration),
                             'refresh_token': user.refresh_token
                              })


@app.route('/users-only/')
def secret():
    '''handles session tokens'''
    success, resp  = extract_token(request)
    if not success:
        return failure_response(resp)
    else:
        session_token = resp
    user = get_user_by_session_token(session_token)
    if not user:
        return failure_response('Invalid session token')
    if not user.verify_session_token(session_token): #if expired
        return failure_response('Expired session token; please renew session')
    if not user.email in _logged_in:
        return failure_response('User not logged in; please log in')
    return success_response({'secret': _secret})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)