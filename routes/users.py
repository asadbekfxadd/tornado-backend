from flask import Blueprint, request, jsonify
from extensions import db
from models.models import User

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["POST"])
def create_or_get_user():
    data = request.json
    tid = data.get("telegram_id")
    if tid:
        u = User.query.filter_by(telegram_id=str(tid)).first()
        if u:
            return jsonify({"id": u.id, "name": u.name})
    u = User(name=data.get("name", "Атлет"), weight=data.get("weight"), height=data.get("height"))
    db.session.add(u)
    db.session.commit()
    return jsonify({"id": u.id, "name": u.name}), 201

@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    u = User.query.get_or_404(user_id)
    data = request.json
    db.session.commit()
    return jsonify({"id": u.id, "name": u.name})
