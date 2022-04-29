""" configure routes for song """
import csv
import logging
import os

from flask import Blueprint, render_template, abort, url_for, current_app
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename, redirect
from app.db import db
from app.db.models import Song
from app.songs.forms import csv_upload

songs = Blueprint('songs', __name__,
                  template_folder='templates')


@songs.route('/songs', methods=['GET'], defaults={"page": 1})
@songs.route('/songs/<int:page>', methods=['GET'])
def songs_browse(page):
    """ display list of songs """
    per_page = 1000
    pagination = Song.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    try:
        return render_template('browse_songs.html', data=data, pagination=pagination)
    except TemplateNotFound:
        abort(404)


@songs.route('/songs/upload', methods=['POST', 'GET'])
@login_required
def songs_upload():
    """ use form to upload song list CSV """
    log = logging.getLogger("upload_songs")
    form = csv_upload()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        list_of_songs = []
        with open(filepath, encoding="utf-8") as file:
            log.info("[%s] opened and parsing filepath:[%s]",
                     current_user, filepath)
            csv_file = csv.DictReader(file)

            # TODO check CSV for proper headers
            csv_header = Song.csv_headers()
            for row in csv_file:
                title = row[csv_header[0]]
                artist = row[csv_header[1]]
                year = row[csv_header[2]]
                genre = row[csv_header[3]]
                list_of_songs.append(Song(title, artist, year, genre))

        current_user.songs = list_of_songs  # pylint: disable=assigning-non-slot
        db.session.commit()

        return redirect(url_for('songs.songs_browse'))
    else:
        log.info("form failed validation")

    try:
        return render_template('upload.html', form=form)
    except TemplateNotFound:
        abort(404)