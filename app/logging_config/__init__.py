""" logging configuration file """
import logging
from logging.config import dictConfig
import os
import json
import flask
import flask
import app
from app import config


log_con = flask.Blueprint('log_con', __name__)

@log_con.before_app_request
def before_request_logging():
    """ log before request """

    # log to myapp.log
    log = logging.getLogger("myApp")
    log.info("My App Logger")


@log_con.after_app_request
def after_request_logging(response):
    """ log after request to request.log and myapp.log """

    # skip logging for below
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response
    elif request.path.startswith('/bootstrap'):
        return response

    # log to request.log
    log = logging.getLogger("request")
    log.info('Response status:' +
        response.status)

    log = logging.getLogger("myApp")
    log.info("My App Logger")
    return response


@log_con.before_app_first_request
def setup_logs():
    """ before app startup logging config """
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, 'logging_config.json')
    with open(filepath, encoding="utf-8") as file:
        logging_config = json.load(file)

    add_path_to_logfile(logging_config)

    # set the name of the apps log folder to logs
    logdir = config.Config.LOG_DIR
    # make a directory if it doesn't exist
    if not os.path.exists(logdir):
        os.mkdir(logdir)

    # configure logger with JSON file
    logging.config.dictConfig(logging_config)

    # log to logfile misc_debug.log
    log = logging.getLogger("misc_debug")
    log.debug("Just configured logging")

    # log to logfile myapp.log
    log = logging.getLogger("myApp")
    log.info("Before app first request")


def add_path_to_logfile(logging_config):
    """ add logging path to logging filename """
    logdir = app.config.Config.LOG_DIR
    handlers = logging_config['handlers']
    for handler_key in handlers:
        handler = handlers[handler_key]
        if 'filename' in handler:
            log_filename = os.path.join(logdir, handler['filename'])
            logging_config['handlers'][handler_key]['filename'] = log_filename