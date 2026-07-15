from flask import Blueprint # type: ignore

from api_auth_utils import role_required

officer_bp = Blueprint('officer', __name__, url_prefix='/api/officer')


# Example of the pattern to follow — matches '/officer/workers':
#
# @officer_bp.route('/workers', methods=['GET'])
# @role_required('Officer')
# def manage_workers():
#     ...
