from flask import Blueprint # type: ignore

from api_auth_utils import role_required

worker_bp = Blueprint('worker', __name__, url_prefix='/api/worker')


# Example of the pattern to follow — matches '/worker/tasks':
#
# @worker_bp.route('/tasks', methods=['GET'])
# @role_required('Worker')
# def assigned_tasks():
#     ...
