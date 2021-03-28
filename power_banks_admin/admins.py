from flask import Blueprint, jsonify
from .auth import loginRequired, getAdminIdFromSession
from .config import ADMIN_ROLE, ADMIN_STATUS
from .db import Admin
from .common import getDictKeyByValue

bp = Blueprint('admins', __name__)


@bp.route('/admins/profile', methods=['GET'])
@loginRequired(ADMIN_ROLE['admin'])
def getProfile():

    admin = Admin.query.get(getAdminIdFromSession())

    profileData = {
        'id': admin.id,
        'email': admin.email,
        'name': admin.name,
        'surname': admin.surname,
        'role': getDictKeyByValue(ADMIN_ROLE, admin.role),
        'status': getDictKeyByValue(ADMIN_STATUS, admin.status)
    }

    return jsonify(profileData)
