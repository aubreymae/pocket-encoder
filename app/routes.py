from flask import Blueprint, jsonify, request

api = Blueprint("api", __name__)

@api.route("/process", methods=["POST"])
def process_video():
    return jsonify({"status": "queued"}), 200