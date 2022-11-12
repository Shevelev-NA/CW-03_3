"""Выполняем экспорт внешних модулей"""
from json import JSONDecodeError

from flask import render_template, request, Blueprint, redirect
import logging

import functions
from functions import *

# JSONDecodeError - дл обработки ошибок во внешнем файле данных
# render_template - служит для работы с шаблонами html
# request - служит для обработки запросов из файлов

# app_api = Blueprint('app_api', __name__)
api_logger = logging.getLogger("api_logger") # Логирование работы


"""Задаем имя  модулю Blueprint"""
main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates_name')

# template_folder - путь на папку с шаблонами HTML
# main_blueprint =  задаем название в текущем файле данного Blueprint
# "main_blueprint" - имя  Blueprint , которое будет суффиксом ко всем именам методов , данного модуля
# __name__ нужно нам для того , чтобы программа понимала , что искать папку шаблонов нужно относительно текущего каталога
# static_folder= путь на каталог статических данных (не обязательный параметр)

"""Вывод формы на главной странице при обращении к '/' """
@main_blueprint.route('/')
def main_page():
    bookmarks_count =functions.bookmarks_count()
    posts_data = functions.get_text_without_tags_string_crop(post_data()) # Перечень всех постов (короткое описание)
    return render_template('./index.html', posts=posts_data, bookmarks_count=bookmarks_count)



""" Создайте представление для одного поста  """
@main_blueprint.route('/post/<int:postid>')
def post_page(postid:int):
    posts_data = post_data()
    try:
        output_post = functions.get_post_by_pk(posts_data, postid) # получаем определенный пост по его индифекатору
    except ValueError:
        return "Такой индификационный номер поста не найден"

    output_comments = functions.get_comments_by_post_id(postid) #  поучаем комментарии определенного  поста через ID поста
    comment_quantity = functions.comments_count(postid) #подсчет кол-ва комментариев

    content = get_text_without_tags(output_post)  # получаем значение content  без символа #

    return render_template("./post.html", post=output_post, comments=output_comments, quantity=comment_quantity, content=content)


""" Создайте представление для определенного пользователя  """
@main_blueprint.route('/user-feed/<user_name>')
def get_posts_by_user(user_name):
    posts_data = functions.get_text_without_tags_string_crop(post_data()) # Перечень всех постов (короткое описание) без тегов
    try:
        output_post = functions.get_posts_by_user(posts_data, user_name)  # получаем определенные посты по имени пльзователя
    except ValueError:
        return "Такой пользователь  не найден"

    return render_template("./user-feed.html", posts=output_post)


""" Поиск и вывод постов при обращении на /search/?s=<ключ поиска> """
@main_blueprint.route('/search/')
def search_page():
    search_query = request.args.get('s', '')  # Получаем введеное слова для поиска через переменную (прописывать в Html ее не обязательно тут )
    """ВЫполняем проверку на ошибки"""
    try:
        """Возвращаем перечень постов которые содерждат слово поиска. Поиск идет по всем постам"""
        posts_data_with_query = search_for_posts(post_data(), search_query)
    except FileNotFoundError:
        logging.error("Файл не найден")
        return "Файл не найден"
    except JSONDecodeError:
        logging.error("Невалидный файл")
        return "Невалидный файл"

    """ Выводит короткое описание найденныйх постов"""
    posts_data = functions.get_text_without_tags_string_crop(posts_data_with_query)

    len_posts_data = len(posts_data_with_query) # Подсчет кооличества постов которые содержат слово для поиска


    return render_template("./search.html", posts=posts_data, len_posts_data=len_posts_data, s=search_query)

# request.arg.get - Пары ключ/значение в строке запроса URL и из GET-формы
# s - имя переменной (ключ) которое присвается вводимой информации в строке запроса
# query= и posts= имена переменных используемых в файле post_list.html т.е мы связывем переменные
# ВАЖНО при добавлении шаблонов , контролировать что путь к папке связан с шаблоном


""" Поиск и вывод постов при обращении  к тегам   """
@main_blueprint.route('/tag/<tag_name>')
def get_posts_by_tag(tag_name):
    api_logger.info("Вывод результатов поиска по тегам в консоли")

    """ Получаю список всех постов и их тегов"""
    posts_data_with_tag = get_text_without_tags_string_crop(post_data())

    """ Возвращает перечень постов c коротким описанием по определенному тегу"""
    try:
        output_post = search_for_posts_by_teg(posts_data_with_tag, tag_name)
    except ValueError:
        return "Такой тег  не найден"
    return render_template("./tag.html", posts=output_post, s=tag_name)


""" Добавление постов в закладки  """
@main_blueprint.route('/bookmarks/add/<postid>')
def add_bookmark(postid):
    try:
        postid = int(postid)
    except:
        logging.error(f"Указан не верный ID")
        return redirect("/", code=302)

    if write_json(postid) is True:
        logging.info(f"Пост c ID №{postid} уже есть в закладках")
        return redirect("/", code=302)
    else:
        write_json(postid)
        logging.info(f"Пост c ID №{postid} добавлен в закладки")
        return redirect("/", code=302) # код перенаправления 302


""" Удаление постов из закладок """
@main_blueprint.route('/bookmarks/remove/<postid>')
def remove_bookmark(postid):
    try:
        postid = int(postid)
    except ValueError:
        logging.error(f"Указан не верный ID")

    remove_json(postid)
    logging.info(f"Пост c ID №{postid} удалЁн из закладок")

    return redirect("/bookmarks/", code=302) # код перенаправления 302


""" Создаем представление закладок """
@main_blueprint.route('/bookmarks/')
def bookmarks_page():
    posts_data = functions.get_text_without_tags_string_crop(bookmarks_data())  # Перечень всех постов (короткое описание)
    return render_template("bookmarks.html", posts=posts_data)

