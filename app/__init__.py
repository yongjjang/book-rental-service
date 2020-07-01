from flask import Flask, request, jsonify, current_app, render_template
from .process_data import *
from .models import *
from .user import user
from .book import book
from .rent import rent
import logging


logging.basicConfig(level=logging.INFO)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(user)
    app.register_blueprint(book)
    app.register_blueprint(rent)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['LOGGING_LEVEL'] = logging.DEBUG
    app.config['SECRET_KEY'] = 'this is secret!!'
    return app


app = create_app()


@app.route('/')
def index():
    return render_template('index.html')
