from flask import flash, redirect, render_template, request
from . import app, db
from .forms import YaсutForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Функция представления главной страницы."""
    form = YaсutForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = get_unique_short_id()
        elif URLMap.query.filter_by(short=custom_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('add_yacut.html', form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=custom_id,
        )
        db.session.add(url_map)
        db.session.commit()
        flash(f'Ваша новая ссылка готова: '
              f'<a href="{request.base_url}{custom_id}">'
              f'{request.base_url}{custom_id}</a>')
    return render_template('add_yacut.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def yacut_redirect(short):
    """
    Функция переадресации на исходный адрес
    при обращении к коротким ссылкам.
    """
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original)
