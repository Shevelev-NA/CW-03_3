"""Выполняем экспорт внешних модулей"""
import json
import logging

POSTS_PATH = "data/posts.json"
COMMENTS_PATH = "data/comments.json"
BOOKMARKS_PATH = "data/bookmarks.json"
# Файл путь относительный потомучто файл  расположен в одном каталоге

logging.basicConfig(level=logging.INFO)

""" Подключаем внешний файл с перечнем постов """
def post_data() -> list[dict]:
    # logging.info("Подключаем внешний файл с перечнем постов")
    with open(POSTS_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)

""" Подключаем внешний файл с перечнем комментариев """
def comments_data() -> list[dict]:
    # logging.info("Подключаем внешний файл с перечнем комментариев")
    with open(COMMENTS_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)

""" Подключаем внешний файл с перечнем закладок """
def bookmarks_data() -> list[dict]:
    # logging.info("Подключаем внешний файл с перечнем закладок")
    with open(BOOKMARKS_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)


""" Функция  возвращает все посты"""
def get_posts_all() -> list[dict]:
    logging.info("Функция  возвращает все посты")
    output_post = []  # создаем новый список для результатов поиска
    for post in post_data():
        output_post.append(post)
    return output_post


""" Функция  возвращает посты определенного пользователя"""
def get_posts_by_user(post_data, user_name: str) -> list[dict]:
    logging.info("Поиск поста по пользователю")
    is_exists = False #проверка на ошибку
    output_post = []  # создаем новый список для результатов поиска
    for post in post_data:
        if user_name.lower().strip() == post['poster_name'].lower():
            is_exists = True
            output_post.append(post)
    if not is_exists:
        raise ValueError("Такой пользователь не найден, измените параметры поиска")
    return output_post



""" Функция  возвращает комментарии определенного поста его ID"""
def get_comments_by_post_id(post_id: int) -> list[dict]:
    logging.info("Функция  возвращает комментарии определенного поста")
    output_post = []  # создаем новый список для результатов поиска
    for comments in comments_data():
        if post_id == comments['post_id']:
            output_post.append(comments)
    return output_post




""" Функция  возвращает ID пользователя  по его user_name"""
def get_id_by_user_name(post_data, user_name) -> list[dict]:
    logging.info("Функция  возвращает ID пользователя  по его user_name")
    for user_id_by in post_data:
        if user_name == user_id_by["poster_name"]:
            return user_id_by["pk"]
    raise "Такой пользователь не найден"


""" Функция  возвращает список постов по ключевому слову"""
def search_for_posts(post_data, query: str) -> list[dict]:
    logging.info("Поиск поста по слову")
    is_exists = False #проверка на ошибку
    result = []  # создаем новый список для результатов поиска
    for post in post_data:
        if query.lower() in post['content'].lower():
            is_exists = True
            result.append(post)
    if not is_exists:
        return result
    return result



""" Функция  возвращает один пост по его идентификатору."""
def get_post_by_pk(post_data, pk: int) -> dict:
    logging.info("Функция  возвращает один пост по его идентификатору")
    output_post = {}  # создаем новый список для результатов поиска
    for post_pk in post_data:
        if pk == post_pk['pk']:
            output_post = post_pk
    return output_post



""" Поиск тегов в  тексте поста """
def get_tags(post:dict) -> list:
    tags = [] # создаем список куда будем складывать теги
    tags_temp = [] # создаем временный список куда будем складывать теги

    words = post["content"].split(" ") # разделяем текст на отдельные слова через пробел
    for word in words:  # перебираем каждое слова и ищем теги
        if "#" in word:
            tag = word.replace("#", "")  # удаляем символ тега
            tags_temp.append(tag)
    for word in tags_temp:  # перебираем каждое слово с тегом  и убираем лишний символ
        if "!" in word:
            tag = word.replace("!", "")  # удаляем символ
            tags.append(tag)
        elif "," in word:
            tag = word.replace(",", "")  # удаляем символ
            tags.append(tag)
        elif "." in word:
            tag = word.replace(".", "")  # удаляем символ
            tags.append(tag)
        else:
            tags.append(word)
    return tags
# print(get_tags(get_post_by_pk(post_data(), 1)))


""" Функция сокращения строки до 50 символов и удаление тегов в тексте"""
def get_text_without_tags_string_crop(post_data) -> list:
    string_post = [] # итоговый список постов
    for post in post_data:

        tags = get_tags(post) # поиск тегов в посте

        text = []
        words = post["content"][:50].split(" ") # разделяем текст на отдельные слова через пробел

        for word in words:  # перебираем каждое слова и ищем теги
            if "#"in word:
                tag = word.replace("#", "")  # удаляем символ тега
                text.append(tag)
            else:
                text.append(word)

            text_clear = " ".join(text) #собираем обратно  из слов предложение
            post["content"] = text_clear # задаю новое значение позиции content
            post["tag"] = tags #добавляю теги в список постов
        string_post.append(post) # собираю обратно посты с корректированным описанием (без тегов)

    return string_post

# for i in get_text_without_tags_string_crop(post_data()):
#     print(i)

""" Функция  возвращает СПИСОК постов по тегу"""
def search_for_posts_by_teg(post_data, query: str) -> list[dict]:
    is_exists = False #проверка на ошибку
    result = []  # создаем новый список для результатов поиска

    for post in post_data:
        for tag_post in post['tag']: # Прохожусь циклом потомучто это список тегов
            if query.lower() == tag_post.lower(): # ПРоверяю на совпадение при этом делаю одинаковый регистр слова
                is_exists = True
                result.append(post)
    if not is_exists:
        return result

    return result

# print(search_for_posts_by_teg(get_text_without_tags_string_crop(post_data()),"1212"))


""" Функция подсчета колличества комментариев к определенному посту по его ID"""
def comments_count(post_id) -> str:
    logging.info("Функция подсчета колличества комментариев к определенному посту по его ID")

    comments_match = []
    text = "комментарий"
    is_exists = False #проверка на ошибку если такого поста нет
    for comment in comments_data():
        if comment['post_id'] == post_id:
            is_exists = True #Значение истина если пост найден (id)
            comments_match.append(comment['pk'])
    if len(comments_match)>0 and len(comments_match) % 2 == 0 or len(comments_match) in [3]:
        text = "комментария"
    elif len(comments_match)  == 1 :
        text = "комментарий"
    elif len(comments_match) in [0, 5, 6,7,8,9,10,11,12]:
        text = "комментариев"

    return f"{len(comments_match)} {text}"




""" Поиск тегов и чистка текста тексте поста """
def get_text_without_tags(post:dict) -> list:
    logging.info("Удаляем из текста знак тегов #")
    text = []
    words = post["content"].split(" ") # разделяем текст на отдельные слова через пробел
    for word in words:  # перебираем каждое слова и ищем теги
        if "#" in word:
            tag = word.replace("#", "")  # удаляем символ тега
            text.append(tag)
        else:
            text.append(word)
    text_clear = " ".join(text)
    return text_clear

# print(get_text_without_tags(get_post_by_pk(post_data(),7)))


""" Функция добавления постав в файл"""
def write_json(postid):
    posts = post_data()  # загружаем существующие посты
    bookmarks = []

    """  открываем файл с закладками и проверяем есть ли уже такой пост"""

    for bookmark in bookmarks_data():
        bookmarks.append(bookmark)
        if postid == bookmark['pk']:
            return True

    for post in posts:
        if postid == post["pk"]:
            bookmarks.append(post) #Добавляем новый пост в закладки

    # for post in posts:
    #     if postid == post["pk"]:
    #         bookmarks.append(post)  # Добавляем новый пост в закладки

    """ перезапись существующего файла с закладками """
    with open(BOOKMARKS_PATH, 'w', encoding='utf-8') as file:
        json.dump(bookmarks, file, ensure_ascii=False)
    return  False


# write_json(6)



""" Функция удаления поста из файла """
def remove_json(postid):
    bookmarks = []

    """  открываем файл с закладками и проверяем есть ли  такой пост"""
    for bookmark in bookmarks_data():
        if bookmark['pk']  != postid:
            bookmarks.append(bookmark)

    """ перезапись существующего файла с закладками """
    with open(BOOKMARKS_PATH, 'w', encoding='utf-8') as file:
        json.dump(bookmarks, file, ensure_ascii=False)
    return
# remove_json(1) #для теста функции


""" Функция подсчета колличества постов в закладках"""
def bookmarks_count() -> int:
    logging.info("Функция подсчета колличества постов в закладках")
    return len(bookmarks_data())

# print(bookmarks_count())


#СТАРОЕ не использую
""" Функция для сохранения картинки"""
def save_picture(picture) -> str:
    filename = picture.filename  # получаем имя фаила
    # методы .filename будет работать только после применениее функции request.files.get('picture')
    # или  request.form.get('content')
    # /uploads/images/ - это стандартные наименования папок (по умолчанию)
    path = f'./uploads/images/{filename}'  # задаем путь для сохранения файла картинки

    picture.save(path)  # так же будет работать только после применения request.files.get или request.form.get
    return path  # Возвращаем путь картинки





#СТАРОЕ не использую

# """ Функция сокращения строки до 50 символов """
# def string_crop()->list:
#     logging.info("Функция сокращения строки до 50 символов")
#     string_post = []
#     for post in post_data():
#         post["content"] = post["content"][:50]
#         string_post.append(post)
#     return string_post


# """ Поиск тегов во всех постах """
# def get_all_tags(post_data, pk) -> list:
#     tags_temp = [] # создаем временный список куда будем складывать теги
#     tags = []
#     for post in post_data:
#         if post["pk"] == pk:
#                 words = post["content"].split(" ") # разделяем текст на отдельные слова через пробел
#                 for word in words:  # перебираем каждое слова и ищем теги
#                     if "#" in word:
#                         tag = word.replace("#", "")  # удаляем символ тега
#                         tags_temp.append({"poster_name":post["poster_name"], "pk":post["pk"], "tag":tag})
#     for word in tags_temp:  # перебираем каждое слово с тегом  и убираем лишний символ
#         word_one = word["tag"]
#         if "." in word_one:
#             tag = word_one.replace(".", "")  # удаляем символ
#             tags.append({"poster_name":word["poster_name"], "pk":word["pk"], "tag":tag})
#         elif "!" in word_one:
#             tag = word_one.replace("!", "")  # удаляем символ
#             tags.append({"poster_name":word["poster_name"], "pk":word["pk"], "tag":tag})
#         elif "," in word_one:
#             tag = word_one.replace(",", "")  # удаляем символ
#             tags.append({"poster_name":word["poster_name"], "pk":word["pk"], "tag":tag})
#         else:
#             tags.append({"poster_name":word["poster_name"], "pk":word["pk"], "tag":word["tag"]})
#     return tags
# # print(get_all_tags(post_data(),2))


#СТАРОЕ не использую

# """ Функция  возвращает комментарии определенного поста по его user_name"""
# def get_comments_by_post_user_name(user_name) -> list[dict]:
#     logging.info("Функция  возвращает комментарии определенного поста по имени пользователя")
#     output_post = []  # создаем новый список для результатов поиска
#     for user_id_by in post_data():
#         if user_name == user_id_by["poster_name"]:
#             for comments in comments_data():
#                 if user_id_by["pk"] == comments['post_id']:
#                     output_post.append(comments)
#     return output_post