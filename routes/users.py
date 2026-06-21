from flask import Blueprint, request, jsonify
from extensions import db
from models.models import User

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["POST"])
def create_or_get_user():
    data = request.json
    phone = data.get("phone")
    if phone:
        u = User.query.filter_by(phone=str(phone)).first()
        if u:
            return jsonify({"id": u.id, "name": u.name})
    u = User(
        name=data.get("name", "Атлет"),
        email=data.get("email"),
        phone=str(phone) if phone else None,
        language=data.get("language", "ru")
    )
    db.session.add(u)
    db.session.commit()
    return jsonify({"id": u.id, "name": u.name}), 201

@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    u = User.query.get_or_404(user_id)
    data = request.json
    if "name" in data: u.name = data["name"]
    if "language" in data: u.language = data["language"]
    db.session.commit()
    return jsonify({"id": u.id, "name": u.name})

@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    u = User.query.get_or_404(user_id)
    return jsonify(u.to_dict())
