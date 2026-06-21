from flask import Blueprint, request, jsonify
from extensions import db
from models.models import Discipline, Lesson

disciplines_bp = Blueprint("disciplines", __name__)

SEED_DATA = [
    {"slug": "mma", "name_ru": "ММА", "name_uz": "MMA", "name_en": "MMA", "description_ru": "Смешанные боевые искусства", "description_uz": "Aralash jangovar sanat", "description_en": "Mixed martial arts", "icon": "X", "order": 1},
    {"slug": "kickboxing", "name_ru": "Кикбоксинг", "name_uz": "Kikboksing", "name_en": "Kickboxing", "description_ru": "Удары руками и ногами", "description_uz": "Qol va oyoq urishlari", "description_en": "Punches and kicks", "icon": "Y", "order": 2},
    {"slug": "muaythai", "name_ru": "Муай Тай", "name_uz": "Muay Tay", "name_en": "Muay Thai", "description_ru": "Тайский бокс", "description_uz": "Tailand boksi", "description_en": "Thai boxing", "icon": "Y", "order": 3},
    {"slug": "judo", "name_ru": "Дзюдо", "name_uz": "Judo", "name_en": "Judo", "description_ru": "Броски и борьба", "description_uz": "Tashlash va kurash", "description_en": "Throws and grappling", "icon": "Z", "order": 4},
]

LESSONS_DATA = [
    {"discipline_slug": "mma", "title_ru": "Базовая стойка", "title_uz": "Asosiy turish", "title_en": "Basic stance", "description_ru": "Правильная стойка — основа всего.", "description_uz": "Togri turish asosi.", "description_en": "Proper stance is the foundation.", "level": "beginner", "is_free": True, "order": 1, "duration_seconds": 300},
    {"discipline_slug": "mma", "title_ru": "Джеб и кросс", "title_uz": "Jab va kross", "title_en": "Jab and cross", "description_ru": "Два главных удара в боксе.", "description_uz": "Boksda ikkita asosiy zarba.", "description_en": "Two main punches in boxing.", "level": "beginner", "is_free": True, "order": 2, "duration_seconds": 420},
    {"discipline_slug": "mma", "title_ru": "Связка 1-2-3", "title_uz": "1-2-3 kombinatsiya", "title_en": "Combination 1-2-3", "description_ru": "Джеб-кросс-хук на лапах.", "description_uz": "Jab-kross-xuk.", "description_en": "Basic jab-cross-hook combo.", "level": "beginner", "is_free": False, "order": 3, "duration_seconds": 480},
    {"discipline_slug": "mma", "title_ru": "Защита и уклоны", "title_uz": "Himoya va qochish", "title_en": "Defense and slips", "description_ru": "Блоки и уклоны.", "description_uz": "Bloklar va qochishlar.", "description_en": "Blocks and slips.", "level": "intermediate", "is_free": False, "order": 4, "duration_seconds": 540},
    {"discipline_slug": "mma", "title_ru": "Работа в клинче", "title_uz": "Klinchda ishlash", "title_en": "Clinch work", "description_ru": "Контроль в клинче.", "description_uz": "Klinchda nazorat.", "description_en": "Clinch control and exits.", "level": "intermediate", "is_free": False, "order": 5, "duration_seconds": 600},
    {"discipline_slug": "kickboxing", "title_ru": "Удар с разворота", "title_uz": "Aylanma zarba", "title_en": "Spinning kick", "description_ru": "Техника разворота.", "description_uz": "Burilish texnikasi.", "description_en": "Rotation technique.", "level": "beginner", "is_free": True, "order": 1, "duration_seconds": 360},
    {"discipline_slug": "kickboxing", "title_ru": "Лоу-кик", "title_uz": "Lou-kik", "title_en": "Low kick", "description_ru": "Удар по бедру.", "description_uz": "Songa zarba.", "description_en": "Thigh kick.", "level": "beginner", "is_free": True, "order": 2, "duration_seconds": 420},
    {"discipline_slug": "kickboxing", "title_ru": "Хай-кик", "title_uz": "Xay-kik", "title_en": "High kick", "description_ru": "Удар ногой в голову.", "description_uz": "Boshga oyoq zarba.", "description_en": "Head kick.", "level": "intermediate", "is_free": False, "order": 3, "duration_seconds": 480},
    {"discipline_slug": "kickboxing", "title_ru": "Связка руки-ноги", "title_uz": "Qol-oyoq kombinatsiya", "title_en": "Hand-leg combo", "description_ru": "Комбо ударов.", "description_uz": "Zarba kombinatsiyasi.", "description_en": "Combined punches and kicks.", "level": "intermediate", "is_free": False, "order": 4, "duration_seconds": 540},
    {"discipline_slug": "kickboxing", "title_ru": "Спарринг", "title_uz": "Sparing", "title_en": "Sparring", "description_ru": "Тактика спарринга.", "description_uz": "Sparing taktikasi.", "description_en": "Sparring tactics.", "level": "advanced", "is_free": False, "order": 5, "duration_seconds": 660},
    {"discipline_slug": "muaythai", "title_ru": "Удар коленом", "title_uz": "Tizza zarba", "title_en": "Knee strike", "description_ru": "Удар коленом в корпус.", "description_uz": "Tizzaning zarba.", "description_en": "Knee to body and head.", "level": "beginner", "is_free": True, "order": 1, "duration_seconds": 360},
    {"discipline_slug": "muaythai", "title_ru": "Удар локтем", "title_uz": "Tirsak zarba", "title_en": "Elbow strike", "description_ru": "Удар локтем.", "description_uz": "Tirsak zarba.", "description_en": "Elbow technique.", "level": "beginner", "is_free": True, "order": 2, "duration_seconds": 420},
    {"discipline_slug": "muaythai", "title_ru": "Клинч", "title_uz": "Klinch", "title_en": "Clinch", "description_ru": "Контроль в клинче.", "description_uz": "Klinchda nazorat.", "description_en": "Clinch control.", "level": "intermediate", "is_free": False, "order": 3, "duration_seconds": 540},
    {"discipline_slug": "muaythai", "title_ru": "Тип-кик", "title_uz": "Tip-kik", "title_en": "Teep kick", "description_ru": "Прямой удар стопой.", "description_uz": "Togri oyoq zarba.", "description_en": "Straight foot push.", "level": "intermediate", "is_free": False, "order": 4, "duration_seconds": 480},
    {"discipline_slug": "muaythai", "title_ru": "Связка в клинче", "title_uz": "Klinchda kombinatsiya", "title_en": "Clinch combo", "description_ru": "Серия в клинче.", "description_uz": "Klinchda seriya.", "description_en": "Knees and elbows in clinch.", "level": "advanced", "is_free": False, "order": 5, "duration_seconds": 600},
    {"discipline_slug": "judo", "title_ru": "Падение", "title_uz": "Yiqilish", "title_en": "Breakfall", "description_ru": "Правильное падение.", "description_uz": "Togri yiqilish.", "description_en": "Safe falling technique.", "level": "beginner", "is_free": True, "order": 1, "duration_seconds": 360},
    {"discipline_slug": "judo", "title_ru": "Захват", "title_uz": "Ushlash", "title_en": "Grip", "description_ru": "Захват кимоно.", "description_uz": "Kimono ushlash.", "description_en": "Gi grip technique.", "level": "beginner", "is_free": True, "order": 2, "duration_seconds": 420},
    {"discipline_slug": "judo", "title_ru": "Бросок через бедро", "title_uz": "Son orqali tashlash", "title_en": "Hip throw", "description_ru": "О-гоши.", "description_uz": "O-goshi.", "description_en": "O-goshi basic throw.", "level": "beginner", "is_free": False, "order": 3, "duration_seconds": 480},
    {"discipline_slug": "judo", "title_ru": "Подсечка", "title_uz": "Oyoq qoqish", "title_en": "Foot sweep", "description_ru": "Де-аши-харай.", "description_uz": "De-ashi-haray.", "description_en": "De-ashi-harai sweep.", "level": "intermediate", "is_free": False, "order": 4, "duration_seconds": 540},
    {"discipline_slug": "judo", "title_ru": "Удержание", "title_uz": "Ushlab turish", "title_en": "Ground hold", "description_ru": "Осаэкоми.", "description_uz": "Osaekomi.", "description_en": "Osaekomi hold technique.", "level": "intermediate", "is_free": False, "order": 5, "duration_seconds": 600},
]

@disciplines_bp.route("/seed", methods=["POST"])
def seed():
    if Discipline.query.count() > 0:
        return jsonify({"message": "already seeded"})
    slug_to_id = {}
    for d in SEED_DATA:
        disc = Discipline(**d)
        db.session.add(disc)
        db.session.flush()
        slug_to_id[d["slug"]] = disc.id
    for l in LESSONS_DATA:
        slug = l.pop("discipline_slug")
        lesson = Lesson(discipline_id=slug_to_id[slug], **l)
        db.session.add(lesson)
    db.session.commit()
    return jsonify({"message": "seeded", "disciplines": len(SEED_DATA), "lessons": len(LESSONS_DATA)}), 201

@disciplines_bp.route("/", methods=["GET"])
def get_disciplines():
    lang = request.args.get("lang", "ru")
    discs = Discipline.query.order_by(Discipline.order).all()
    return jsonify([d.to_dict(lang) for d in discs])

@disciplines_bp.route("/<slug>/lessons", methods=["GET"])
def get_lessons(slug):
    lang = request.args.get("lang", "ru")
    disc = Discipline.query.filter_by(slug=slug).first_or_404()
    lessons = Lesson.query.filter_by(discipline_id=disc.id).order_by(Lesson.order).all()
    return jsonify([l.to_dict(lang) for l in lessons])

@disciplines_bp.route("/lessons/<int:lesson_id>", methods=["GET"])
def get_lesson(lesson_id):
    lang = request.args.get("lang", "ru")
    lesson = Lesson.query.get_or_404(lesson_id)
    return jsonify(lesson.to_dict(lang))