from flask import Blueprint, request, jsonify
from extensions import db
from models.models import Exercise

exercises_bp = Blueprint("exercises", __name__)

SEEDS = [
    {"name": "Жим штанги лёжа", "muscle_group": "chest", "equipment": "barbell", "description": "Базовое на грудные"},
    {"name": "Жим гантелей лёжа", "muscle_group": "chest", "equipment": "dumbbell", "description": "Грудные"},
    {"name": "Отжимания на брусьях", "muscle_group": "chest", "equipment": "bodyweight", "description": "Грудные трицепс"},
    {"name": "Становая тяга", "muscle_group": "back", "equipment": "barbell", "description": "Базовое"},
    {"name": "Подтягивания", "muscle_group": "back", "equipment": "bodyweight", "description": "Спина"},
    {"name": "Тяга штанги в наклоне", "muscle_group": "back", "equipment": "barbell", "description": "Спина"},
    {"name": "Тяга верхнего блока", "muscle_group": "back", "equipment": "machine", "description": "Широчайшие"},
    {"name": "Приседания со штангой", "muscle_group": "legs", "equipment": "barbell", "description": "Ноги"},
    {"name": "Жим ногами", "muscle_group": "legs", "equipment": "machine", "description": "Квадрицепс"},
    {"name": "Румынская тяга", "muscle_group": "legs", "equipment": "barbell", "description": "Бицепс бедра"},
    {"name": "Жим штанги стоя", "muscle_group": "shoulders", "equipment": "barbell", "description": "Плечи"},
    {"name": "Разводка гантелей стоя", "muscle_group": "shoulders", "equipment": "dumbbell", "description": "Плечи"},
    {"name": "Подъём штанги на бицепс", "muscle_group": "arms", "equipment": "barbell", "description": "Бицепс"},
    {"name": "Французский жим", "muscle_group": "arms", "equipment": "barbell", "description": "Трицепс"},
    {"name": "Планка", "muscle_group": "core", "equipment": "bodyweight", "description": "Кор"},
    {"name": "Скручивания", "muscle_group": "core", "equipment": "bodyweight", "description": "Пресс"},
]

@exercises_bp.route("/seed", methods=["POST"])
def seed_exercises():
    if Exercise.query.count() > 0:
        return jsonify({"message": "already seeded"})
    for ex in SEEDS:
        db.session.add(Exercise(**ex))
    db.session.commit()
    return jsonify({"message": "seeded", "count": len(SEEDS)}), 201

@exercises_bp.route("/", methods=["GET"])
def get_exercises():
    mg = request.args.get("muscle_group")
    q = Exercise.query
    if mg:
        q = q.filter_by(muscle_group=mg)
    exs = q.order_by(Exercise.name).all()
    return jsonify([{"id": e.id, "name": e.name, "muscle_group": e.muscle_group, "equipment": e.equipment} for e in exs])

@exercises_bp.route("/search", methods=["GET"])
def search_exercises():
    q = request.args.get("q", "")
    exs = Exercise.query.filter(Exercise.name.ilike(f"%{q}%")).limit(20).all()
    return jsonify([{"id": e.id, "name": e.name, "muscle_group": e.muscle_group, "equipment": e.equipment} for e in exs])
