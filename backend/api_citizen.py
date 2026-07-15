from flask import Blueprint # type: ignore

from api_auth_utils import role_required

citizen_bp = Blueprint('citizen', __name__, url_prefix='/api/citizen')


# Example of the pattern to follow once you're ready to add real routes —
# matches the corresponding frontend route '/citizen/complaints':
#
# @citizen_bp.route('/complaints', methods=['GET'])
# @role_required('Citizen')
# def my_complaints():
#     from flask_jwt_extended import get_jwt_identity
#     from models import Complaint
#     user_id = get_jwt_identity()
#     complaints = Complaint.query.filter_by(created_by=int(user_id)).all()
#     return jsonify(success=True, complaints=[...]), 200
