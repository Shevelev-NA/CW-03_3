"""Выполняем экспорт внешних модулей"""
from json import JSONDecodeError

from flask import render_template, request, Blueprint
import logging
from functions import get_posts_by_word

# JSONDecodeError - дл обработки ошибок во внешнем файле данных
# render_template - служит для работы с шаблонами html
# request - служит для обработки запросов из файлов



"""Задаем имя  модулю Blueprint"""
main_blueprint = Blueprint('main_blueprint', __name__, template_folder='Templates_name', static_folder='static')

# template_folder - путь на папку с шаблонами HTML
# main_blueprint =  задаем название в текущем файле данного Blueprint
# "main_blueprint" - имя  Blueprint , которое будет суффиксом ко всем именам методов , данного модуля
# __name__ нужно нам для того , чтобы программа понимала , что искать папку шаблонов нужно относительно текущего каталога
# static_folder= путь на каталог статических данных (не обязательный параметр)

"""Вывод формы на главной странице при обращении к '/' """


@main_blueprint.route('/')
def main_page():
    return render_template('index.html')


""" Поиск и вывод постов при обращении на /search/?s=<ключ поиска> """


@main_blueprint.route('/search/')
def search_page():
    search_query = request.args.get('s', '')
    """ВЫполняем проверку на ошибки"""
    try:
        posts = get_posts_by_word(search_query)

    except FileNotFoundError:
        logging.error("Файл не найден")
        return "Файл не найден"
    except JSONDecodeError:
        logging.error("Невалидный файл")
        return "Невалидный файл"
    return render_template('post_list.html', posts=posts)

# request.arg.get - Пары ключ/значение в строке запроса URL и из GET-формы
# s - имя переменной (ключ) которое присвается вводимой информации в строке запроса
# query= и posts= имена переменных используемых в файле post_list.html т.е мы связывем переменные
# ВАЖНО при добавлении шаблонов , контролировать что путь к папке связан с шаблоном
