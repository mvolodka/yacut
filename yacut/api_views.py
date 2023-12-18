from http import HTTPStatus
from re import match

from flask import jsonify, request
from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/<string:short>/', methods=['GET'])
def yacut_redirect_api(short):
    """
    GET-запрос на получение оригинальной ссылки
    по указанному короткому идентификатору.
    """
    redirect = URLMap.query.filter_by(short=short).first()
    if not redirect:
        raise InvalidAPIUsage(
            'Указанный id не найден',
            HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': redirect.original})


@app.route('/api/id/', methods=['POST'])
def create_short_api():
    """
    POST-запрос на создание новой короткой ссылки.
    """
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса'
        )
    if 'url' not in data:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!'
        )
    if not data.get('custom_id'):
        data['custom_id'] = get_unique_short_id()
    elif URLMap.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    elif not match(r'^[A-Za-z0-9_]{1,16}$', data['custom_id']):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки'
        )
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
