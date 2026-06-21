from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    language = db.Column(db.String(5), default="ru")
    is_subscribed = db.Column(db.Boolean, default=False)
    subscription_until = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "language": self.language,
            "is_subscribed": self.is_subscribed,
        }

class Discipline(db.Model):
    __tablename__ = "disciplines"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    name_ru = db.Column(db.String(100), nullable=False)
    name_uz = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    description_ru = db.Column(db.Text)
    description_uz = db.Column(db.Text)
    description_en = db.Column(db.Text)
    icon = db.Column(db.String(10), default="🥊")
    order = db.Column(db.Integer, default=0)
    lessons = db.relationship("Lesson", backref="discipline", lazy=True)

    def to_dict(self, lang="ru"):
        name = self.name_ru if lang == "ru" else (self.name_uz if lang == "uz" else self.name_en)
        desc = self.description_ru if lang == "ru" else (self.description_uz if lang == "uz" else self.description_en)
        return {
            "id": self.id,
            "slug": self.slug,
            "name": name,
            "description": desc,
            "icon": self.icon,
            "lesson_count": len(self.lessons)
        }

class Lesson(db.Model):
    __tablename__ = "lessons"
    id = db.Column(db.Integer, primary_key=True)
    discipline_id = db.Column(db.Integer, db.ForeignKey("disciplines.id"), nullable=False)
    title_ru = db.Column(db.String(200), nullable=False)
    title_uz = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    description_ru = db.Column(db.Text)
    description_uz = db.Column(db.Text)
    description_en = db.Column(db.Text)
    video_url = db.Column(db.String(500))
    thumbnail_url = db.Column(db.String(500))
    duration_seconds = db.Column(db.Integer, default=0)
    level = db.Column(db.String(20), default="beginner")
    is_free = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, lang="ru"):
        title = self.title_ru if lang == "ru" else (self.title_uz if lang == "uz" else self.title_en)
        desc = self.description_ru if lang == "ru" else (self.description_uz if lang == "uz" else self.description_en)
        return {
            "id": self.id,
            "discipline_id": self.discipline_id,
            "title": title,
            "description": desc,
            "video_url": self.video_url,
            "thumbnail_url": self.thumbnail_url,
            "duration_seconds": self.duration_seconds,
            "level": self.level,
            "is_free": self.is_free,
            "order": self.order
        }

class UserProgress(db.Model):
    __tablename__ = "user_progress"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    watched_seconds = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, nullable=True)
