from flask import Flask
from main.views_main import main_blueprint


app = Flask(__name__)

""" Регистрируем блюпринт"""

app.register_blueprint(main_blueprint)  # все страницы в одном файле


app.run()
