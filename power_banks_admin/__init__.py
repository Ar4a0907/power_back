import logging
import traceback
from flask import Flask, request, jsonify
from datetime import timedelta, datetime
import bcrypt
from flask_jwt_extended import create_access_token, get_raw_jwt
from werkzeug.exceptions import HTTPException
from .common import logInfo, logCritical, logError, sqlDebug, encrypt, decrypt, logDebug
from .common import getDictKeyByValue
from .config import ADMIN_STATUS, ADMIN_ROLE, ADMIN_MAX_LOGIN_ATTEMPTS
from .db import db, dbSession, Admin
from . import admins
from .auth import jwt, loginRequired, RevokedTokenAdmin, getAdminIdFromSession
from .validation_schemas.auth_schemas import AuthSchemas


class ConfigClass(object):
    ENVIRONMENT = 'test'  # set whatever else for prod
    BASE_URL = 'http://localhost:3000'

    # Flask settings
    JWT_SECRET_KEY = '9PvSQPKL0geUtrIieeDn498HMt47yJFk'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']  # access token will be checked in blacklist, add refresh for refresh token if required
    JWT_EXPIRATION_TIME = 3  # days

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'  # file-based SQL database for dev only
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # avoids SQLAlchemy warning

    # Flask-User settings
    USER_ENABLE_EMAIL = True  # enable email authentication
    USER_ENABLE_USERNAME = False  # enable username authentication
    DEBUG = True  # MEMO: michael: change to False for production


app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')

if app.config['ENVIRONMENT'] != 'test':
    gunicornLogger = logging.getLogger('gunicorn.error')
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    app.logger.handlers = gunicornLogger.handlers
    app.logger.setLevel(gunicornLogger.level)
else:  # MEMO: michael: used only for dev
    from flask_cors import CORS

    CORS(app)
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    app.logger.setLevel(logging.DEBUG)

    # MEMO: michael: dev use only! turn on SQL queries debug mode, all queries and execution time will be logged
    # app.config['SQLALCHEMY_RECORD_QUERIES'] = True
    # app.after_request(sqlDebug)

db.init_app(app)

app.register_blueprint(admins.bp)

jwt.init_app(app)


@app.route('/admin', methods=['POST'])
# @loginRequired(ADMIN_ROLE['super_admin'])
def signup():
    if ConfigClass.ENVIRONMENT == 'test':
        requestData = request.json

        if 'email' not in requestData or 'password' not in requestData:
            return jsonify({'message': 'Wrong data supplied'}), 400

        if Admin.query.filter_by(email=requestData['email'].lower()).first() is not None:
            return jsonify({'error': 'Email already in use'}), 400

        admin = Admin(email=requestData['email'].lower(),
                      password=bcrypt.hashpw(requestData['password'].encode('utf-8'), bcrypt.gensalt(rounds=12)),
                      name=requestData['name'], surname=requestData['surname'], status=ADMIN_STATUS['confirmed'],
                      role=ADMIN_ROLE['admin'])

        db.session.add(admin)
        db.session.commit()

    return jsonify({'message': 'ok'})


@app.route('/login', methods=['POST'])
def login():

    requestData = request.json

    validation_result = AuthSchemas.validateLogin(requestData)

    if not validation_result['success']:
        return jsonify(validation_result['error']), 400

    admin = Admin.query.filter_by(email=requestData['email'].lower()).first()

    if admin is None:
        return jsonify({'error': 'wrong_data_supplied'}), 400

    if admin.status == ADMIN_STATUS['blocked']:
        return jsonify({'error': 'admin_is_blocked'}), 400

    if admin.status == ADMIN_STATUS['removed']:
        return jsonify({'error': 'admin_not_found'}), 404

    if admin.loginAttempts + 1 == ADMIN_MAX_LOGIN_ATTEMPTS:
        admin.status = ADMIN_STATUS['blocked']
        dbSession.add(admin)
        dbSession.commit()
        return jsonify({'error': 'maximum_login_attempts_reached'}), 400

    if not bcrypt.checkpw(requestData['password'].encode('utf8'), admin.password):
        admin.loginAttempts = admin.loginAttempts + 1
        dbSession.add(admin)
        dbSession.commit()
        return jsonify({'error': 'wrong_data_supplied'}), 400

    admin.loginAttempts = 0

    db.session.add(admin)
    db.session.commit()

    accessToken = create_access_token(identity=admin, expires_delta=timedelta(days=app.config['JWT_EXPIRATION_TIME']))

    return jsonify(accessToken=accessToken, email=admin.email, role=getDictKeyByValue(ADMIN_ROLE, admin.role))


@app.route('/logout', methods=['POST'])
@loginRequired(ADMIN_ROLE['admin'])
def logout():

    jti = get_raw_jwt()['jti']

    try:
        revoked_token = RevokedTokenAdmin(jti=jti)
        revoked_token.add()
        return jsonify({})
    except:
        return jsonify({'error': 'server_error'}), 500


def handleApplicationErrors(e):
    # generate unique error ID
    errorId = None
    adminId = getAdminIdFromSession()

    if adminId is not None:
        errorId = str(adminId) + '_' + str(datetime.utcnow().timestamp())

    logCritical('error occurred; error_id={}, error={}, traceback:\n{}'.format(errorId, e, traceback.format_exc()))

    responseData = {'error': 'server_error'}

    if errorId is not None:
        responseData['errorId'] = errorId

    return jsonify(responseData), 500


@app.errorhandler(Exception)
def handleException(e):
    # return http exceptions as is except 500 and 502 status code
    if isinstance(e, HTTPException) and e.code != 500 and e.code != 502:
        logError('error occurred; error={}'.format(e))
        return e

    return handleApplicationErrors(e)

