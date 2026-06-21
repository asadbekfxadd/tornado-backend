from flask import Blueprint, request, jsonify
from extensions import db
from models.models import Workout, WorkoutSet
from datetime import datetime

workouts_bp = Blueprint("workouts", __name__)

@workouts_bp.route("/", methods=["GET"])
def get_workouts():
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    workouts = Workout.query.filter_by(user_id=user_id).order_by(Workout.started_at.desc()).all()
    return jsonify([w.to_dict() for w in workouts])

@workouts_bp.route("/", methods=["POST"])
def create_workout():
    data = request.json
    workout = Workout(user_id=data["user_id"], name=data.get("name", "Тренировка"), started_at=datetime.utcnow())
    db.session.add(workout)
    db.session.commit()
    return jsonify(workout.to_dict()), 201

@workouts_bp.route("/<int:workout_id>/finish", methods=["POST"])
def finish_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    workout.finished_at = datetime.utcnow()
    db.session.commit()
    return jsonify(workout.to_dict())

@workouts_bp.route("/<int:workout_id>/sets", methods=["POST"])
def add_set(workout_id):
    data = request.json
    s = WorkoutSet(workout_id=workout_id, exercise_id=data["exercise_id"], set_number=data["set_number"], reps=data.get("reps"), weight_kg=data.get("weight_kg"), rest_seconds=data.get("rest_seconds", 90), is_warmup=data.get("is_warmup", False))
    db.session.add(s)
    db.session.commit()
    return jsonify(s.to_dict()), 201

@workouts_bp.route("/<int:workout_id>/sets/<int:set_id>", methods=["PUT"])
def update_set(workout_id, set_id):
    s = WorkoutSet.query.get_or_404(set_id)
    data = request.json
    if "reps" in data: s.reps = data["reps"]
    if "weight_kg" in data: s.weight_kg = data["weight_kg"]
    db.session.commit()
    return jsonify(s.to_dict())

@workouts_bp.route("/<int:workout_id>/sets/<int:set_id>", methods=["DELETE"])
def delete_set(workout_id, set_id):
    s = WorkoutSet.query.get_or_404(set_id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({"ok": True})

@workouts_bp.route("/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    return jsonify(Workout.query.get_or_404(workout_id).to_dict())

@workouts_bp.route("/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    w = Workout.query.get_or_404(workout_id)
    db.session.delete(w)
    db.session.commit()
    return jsonify({"ok": True})
