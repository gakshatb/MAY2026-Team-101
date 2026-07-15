from flask import Blueprint # type: ignore

from api_auth_utils import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


# Example of the pattern to follow — matches '/admin/departmentmanagement':
#
# @admin_bp.route('/departmentmanagement', methods=['GET'])
# @role_required('Admin')
# def department_management():
#     ...
