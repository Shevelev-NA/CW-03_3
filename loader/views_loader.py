"""Выполняем экспорт внешних модулей"""
from json import *
from flask import render_template, request, Blueprint
from functions import *
import logging


"""Задаем имя  модулю Blueprint"""
loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates_loader')


@loader_blueprint.route('/post/')
def add_post_page():
    return render_template('post_form.html')


"""ОБработка запроса по добавлению нового поста"""


@loader_blueprint.route('/post/', methods=['POST', 'GET'])
def add_post():

    picture = request.files.get('picture')
    content = request.form.get('content')

    # по умолчанию выполняется GET и писать его не обязательно, но для понимания лучше добавить

    """ ПРоверка типо загружаемого материала"""

    if not picture or not content:
        return "Нет картинки или текста"
    if picture.filename.lower().split('.')[-1] not in ['jpeg', 'png', 'jpg']:
        logging.error("Неверное расширение файла")

        return 'Неверное расширение файла'

    # .filename. - стандартная функция для определения полного имени файла с расширением split('.') - используем
    # чтобы разделить имя файла (как бы одно слово) на список из двух слов и в качестве разделителя используем точку.
    # [-1] - это применяем чтобы получить первое слово с конца после согдания списка слова из имени файла (имя,
    # расширение) после получения расширения проверяем его в списке допустимых

    """ Проверка на ошиибки при сохранениии файла """
    try:
        picture_path: str = '/' + save_picture(picture)
    except FileNotFoundError:
        return "Файл не найден"
    except JSONDecodeError:
        return "Невалидный файл"

    post: dict = get_post({'pic': picture_path, 'content': content})

    return render_template('post_uploaded.html', post=post)
