from app.services import OptionService

from flask import Blueprint, jsonify


bp = Blueprint('option', __name__)


@bp.route('/options/', methods=['GET'])
def option():
    return jsonify(OptionService.get_options())
