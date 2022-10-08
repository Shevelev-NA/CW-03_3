"""Выполняем экспорт внешних модулей"""
import json
import logging

POSTS_PATH = 'posts.json'
# Файл с перечнем постов, путь относительный потомучто файл  расположен в одном каталоге

logging.basicConfig(level=logging.INFO)

""" Подключаем внешний файл с перечнем постов """
def load_posts() -> list[dict]:
    with open(POSTS_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)


""" Функция для поиска постов по тегу"""
def get_posts_by_word(word: str) -> list[dict]:
    logging.info("Поиск поста")
    result = []  # создаем новый список для результатов поиска
    for post in load_posts():
        if word.lower() in post['content'].lower():
            result.append(post)
    return result


""" Функция для сохранения картинки"""
def save_picture(picture) -> str:
    filename = picture.filename  # получаем имя фаила
    # методы .filename будет работать только после применениее функции request.files.get('picture')
    # или  request.form.get('content')
    # /uploads/images/ - это стандартные наименования папок (по умолчанию)
    path = f'./uploads/images/{filename}'  # задаем путь для сохранения файла картинки

    picture.save(path)  # так же будет работать только после применения request.files.get или request.form.get
    return path  # Возвращаем путь картинки


""" Функция добавления постав в файл"""
def get_post(post: dict) -> dict:
    posts = load_posts()  # загружаем существующие посты
    posts.append(post)  # добавление нового поста

    """ перезапись существующего файла """
    with open(POSTS_PATH, 'w', encoding='utf-8') as file:
        json.dump(posts, file)

    return post
