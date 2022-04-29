""" test logging """

import os
import json
import app.config
from app.logging_config import add_path_to_logfile


def test_logfile_misc_debug():
    """ check if misc_debug.log exists """
    log_dir = app.config.Config.LOG_DIR
    filepath = os.path.join(log_dir, "misc_debug.log")
    assert os.path.isfile(filepath)


def test_logfile_request():
    """ check if misc_debug.log exists """
    log_dir = app.config.Config.LOG_DIR
    filepath = os.path.join(log_dir, "request.log")
    assert os.path.isfile(filepath)


def test_logfile_upload_songs():
    """ check if upload_songs.log exists """
    filepath = os.path.join(app.config.Config.LOG_DIR,'upload_songs.log')
    assert os.path.isfile(filepath)


def test_add_path_to_logfile():
    """ test function to add path to logger filename """
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, '../app/logging_config/logging_config.json')
    with open(filepath, encoding="utf-8") as file:
        logging_config = json.load(file)

    # add logging path to logging filename
    add_path_to_logfile(logging_config)

    flask_log = os.path.join( app.config.Config.LOG_DIR, 'flask.log')
    assert logging_config['handlers']['file.handler']['filename'] == flask_log