from flask import Flask, send_from_directory

from main.views_main import *
from loader.views_loader import *


app = Flask(__name__)

""" Регистрируем блюпринт"""

app.register_blueprint(main_blueprint)  # Главная страница
app.register_blueprint(loader_blueprint) # ОБработка запроса по добавлению нового поста


""" Функция загрузки файолв на сервер в указанную директорию """
@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path) # отправляет файл для загрузки

    # path - путь к файлу относительно каталога uploads

app.run()

