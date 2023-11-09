from flask import Blueprint, jsonify, request
from bot_app.neeeew import chatbot
# from common.extensions import USECASE_TEAM as team

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST'])


def the_predictor():
    print("predictor is working")
    input_from_ui=request.json.get('message')
    print("input_from_ui : "+ input_from_ui)
    opvar=chatbot(input_from_ui)
    print("testing is working")
    return jsonify({"response" : opvar}),200