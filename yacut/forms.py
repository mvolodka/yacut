from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


class YaсutForm(FlaskForm):
    """Форма для добавления ссылки."""
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    URL(require_tld=True, message='Некорректный URL')]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16,
                   message=f'Пользовательский вариант короткой ссылки'
                           f'не должен превышать 16 символов.'),
            Optional(),
            Regexp(r'^[A-Za-z0-9_]+$',
                   message='Имя ссылки содержит недопустимые символы.')
        ]
    )
    submit = SubmitField('Создать')
