from flask import Blueprint, request, jsonify
from extensions import db
from models.models import Discipline, Lesson

disciplines_bp = Blueprint("disciplines", __name__)

SEED_DATA = [
    {
        "slug": "mma",
        "name_ru": "ММА",
        "name_uz": "MMA",
        "description_ru": "Смешанные боевые искусства — полная подготовка бойца",
        "description_uz": "Aralash jangovar san'at — to'liq jangchi tayyorgarligi",
        "icon": "🥊",
        "order": 1
    },
    {
        "slug": "kickboxing",
        "name_ru": "Кикбоксинг",
        "name_uz": "Kikboksing",
        "description_ru": "Удары руками и ногами — техника и связки",
        "description_uz": "Qo'l va oyoq urishlari — texnika va kombinatsiyalar",
        "icon": "🦵",
        "order": 2
    },
    {
        "slug": "muaythai",
        "name_ru": "Муай Тай",
        "name_uz": "Muay Tay",
        "description_ru": "Тайский бокс — колени, локти, клинч",
        "description_uz": "Tailand boksi — tizzalar, tirsak, klinch",
        "icon": "🦵",
        "order": 3
    },
    {
        "slug": "judo",
        "name_ru": "Дзюдо",
        "name_uz": "Judo",
        "description_ru": "Броски и борьба — техника захватов",
        "description_uz": "Tashlash va kurash — ushlash texnikasi",
        "icon": "🤼",
        "order": 4
    }
]

LESSONS_DATA = [
    {"discipline_slug": "mma", "title_ru": "Базовая стойка бойца", "title_uz": "Asosiy jangchi turishi", "description_ru": "Правильная стойка — основа всего. Учимся держать позицию.", "description_uz": "To'g'ri turish — hamma narsaning asosi.", "level": "beginner", "is_free": True, "order": 1, "duration_seconds": 300},
    {"discipline_slug": "mma", "title_ru": "Прямые удары — джеб и кросс", "title_uz": "To'g'ri zarbalar — jab va kross", "description_ru": "Два главных удара в боксе. Разбираем технику детально.", "description_uz": "Boksda ikkita asosiy zarba.", "level": "beginner", "is_free": True, "order": 2, "duration_seconds": 420},
    {"discipline_slug": "mma", "title_ru": "Связка 1-2-3", "title_uz": "1-2-3 kombinatsiyasi", "description_ru": "Базовая связка джеб-кросс-хук. Отрабатываем на лапах.", "description_uz": "Asosiy kombinatsiya jab-kross-xuk.", "level": "beginner", "is_free": False, "order": 3, "duration_seconds": 480},
    {"discipline_slug": "mma", "title_ru": "Защита и уклоны", "title_uz": "Himoya va qochishlar", "description_ru": "Блоки, уклоны, нырки — как не получать удары.", "description_uz": "Bloklar, qochishlar — qanday urmaslik.", "level": "intermediate", "is_free": False, "order": 4, "duration_seconds": 540},
    {"discipline_slug": "mma", "title_ru": "Работа в клинче", "title_uz": "Klinchda ishlash", "description_ru": "Клинч — контроль, удары коленями, выходы.", "description_uz": "Klinch — nazorat, tizza zarbalari.", "level": "intermediate", "is_free": False, "order": 5, "duration_seconds": 600},
    {"discipline_slug": "kickboxing", "title_ru": "Удар с разворота", "title_uz": "Aylanma zarba", "description_ru": "Эффектный удар — техника разворота и вложения.", "description_uz": "Samarali zarba — burilish texnikasi.", "level": "beginner", "is_free": True, "order": 1, "duration_seconds": 360},
    {"discipline_slug": "kickboxing", "title_ru": "Лоу-кик", "title_uz": "Lou-kik", "description_ru": "Удар по бедру — один из самых эффективных в кикбоксинге.", "description_uz": "Songa zarba — kikboksingda eng samarali.", "level": "beginner", "is_free": True, "order": 2, "duration_seconds": 420},
    {"discipline_slug": "kickboxing", "title_ru": "Хай-кик в голову", "title_uz": "Boshga xay-kik", "description_ru": "Удар ногой в голову — техника и растяжка.", "description_uz": "Boshga oyoq zarba — texnika.", "level": "intermediate", "is_free": False, "order": 3, "duration_seconds": 480},
    {"discipline_slug": "kickboxing", "title_ru": "Связка руки-ноги", "title_uz": "Qo'l-oyoq kombinatsiyasi", "description_ru": "Комбинация ударов руками и ногами в серии.", "description_uz": "Qo'l va oyoq zarbalari kombinatsiyasi.", "level": "intermediate", "is_free": False, "order": 4, "duration_seconds": 540},
    {"discipline_slug": "kickboxing", "title_ru": "Спаринг-техника", "title_uz": "Sparing texnikasi", "description_ru": "Как вести себя в спарринге — дистанция, темп, тактика.", "description_uz": "Sparingda qanday harakat qilish.", "level": "advanced", "is_free": False, "order": 5, "duration_seconds": 660},
    {"discipline_slug": "muaythai", "title_ru": "Удар коленом", "title_uz": "Tizza zarba", "description_ru": "Визитная карточка Муай Тай — удар коленом в корпус и голову.", "description_uz": "Muay Tayning belgisi — tizza zarba.", "level": "beginner", "is_free": True, "order": 1, "duration_seconds": 360},
    {"discipline_slug": "muaythai", "title_ru": "Удар локтем", "title_uz": "Tirsak zarba", "description_ru": "Локоть — самое опасное оружие в Муай Тай.", "description_uz": "Tirsak — Muay Taydagi eng xavfli qurol.", "level": "beginner", "is_free": True, "order": 2, "duration_seconds": 420},
    {"discipline_slug": "muaythai", "title_ru": "Клинч Муай Тай", "title_uz": "Muay Tay klinchi", "description_ru": "Контроль в клинче, удары коленями в захвате.", "description_uz": "Klinchda nazorat, tutishda tizza zarbalari.", "level": "intermediate", "is_free": False, "order": 3, "duration_seconds": 540},
    {"discipline_slug": "muaythai", "title_ru": "Тип-удар ногой", "title_uz": "Tip-oyoq zarba", "description_ru": "Тип — прямой удар стопой для остановки атаки.", "description_uz": "Tip — hujumni to'xtatish uchun to'g'ri oyoq zarba.", "level": "intermediate", "is_free": False, "order": 4, "duration_seconds": 480},
    {"discipline_slug": "muaythai", "title_ru": "Связка в клинче", "title_uz": "Klinchda kombinatsiya", "description_ru": "Серия ударов коленями и локтями в клинче.", "description_uz": "Klinchda tizza va tirsak zarbalari seriyasi.", "level": "advanced", "is_free": False, "order": 5, "duration_seconds": 600},
    {"discipline_slug": "judo", "title_ru": "Падение и страховка", "title_uz": "Yiqilish va sug'urta", "description_ru": "Учимся правильно падать — основа безопасности в дзюдо.", "description_uz": "To'g'ri yiqilishni o'rganamiz — judoda xavfsizlik asosi.", "level": "beginner", "is_free": True, "order": 1, "duration_seconds": 360},
    {"discipline_slug": "judo", "title_ru": "Захват и стойка", "title_uz": "Ushlash va turish", "description_ru": "Правильный захват кимоно — контроль соперника.", "description_uz": "To'g'ri kimono ushlash — raqibni nazorat qilish.", "level": "beginner", "is_free": True, "order": 2, "duration_seconds": 420},
    {"discipline_slug": "judo", "title_ru": "Бросок через бедро", "title_uz": "Son orqali tashlash", "description_ru": "О-гоши — один из базовых бросков дзюдо.", "description_uz": "O-goshi — judoning asosiy tashlamalaridan biri.", "level": "beginner", "is_free": False, "order": 3, "duration_seconds": 480},
    {"discipline_slug": "judo", "title_ru": "Подсечка", "title_uz": "Oyoq qoqish", "description_ru": "Де-аши-харай — подсечка под переднюю ногу.", "description_uz": "De-ashi-haray — oldingi oyoqni qoqish.", "level": "intermediate", "is_free": False, "order": 4, "duration_seconds": 540},
    {"discipline_slug": "judo", "title_ru": "Удержание на земле", "title_uz": "Yerda ushlab turish", "description_ru": "Осаэкоми — техники удержания соперника на татами.", "description_uz": "Osaekomi — raqibni tatamida ushlab turish texnikasi.", "level": "intermediate", "is_free": False, "order": 5, "duration_seconds": 600},
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
