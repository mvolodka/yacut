from datetime import datetime

from flask import url_for
from . import db


class URLMap(db.Model):
    """Модель добавления ссылки."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), unique=True, nullable=False)
    short = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Метод-сериализатор."""
        return dict(
            url=self.original,
            short_link=url_for(
                'yacut_redirect',
                short=self.short,
                _external=True
            )
        )

    def from_dict(self, data):
        """Метод-десериализатор."""
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])
