import os
import time
from flask import Blueprint, render_template, request, current_app, send_from_directory, \
    redirect, url_for, flash, abort
from flask.ext.login import login_user, login_required, current_user
from werkzeug import secure_filename
from ..models import User, Image, Category, Extract
from . import gallery
from .forms import ImageForm, CategoryForm, SwitchAlgorithmForm, InvisibleForm, ExtractForm
from app import db

current_path = os.path.abspath('.')
##################################
# The below code for Celery ...
import sys
from celery import Celery
import celeryconfig

results = []
celery = Celery()
celery.config_from_object(celeryconfig)


###############################
# results.append(celery.send_task("tasks.embed_string", [sys.argv[1]]))


@gallery.route('/', methods=['GET', 'POST'])
@gallery.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    if user is None:
        abort(404)
    albums = Category.query.filter_by(author_id=user.id).all()
    if len(albums) == 0:
        flash('You have to create a album!')
        return redirect(url_for('.create_album'))
    size_album = len(albums)
    return render_template('gallery/index.html', size_album=size_album, albums=albums)


@gallery.route('/cm', methods=['GET', 'POST'])
def create_album():
    form = CategoryForm()
    if request.method == 'POST':
        if form.name.data:
            category_name = form.name.data
            user = User.query.filter_by(username=current_user.username).first_or_404()
            if user is None:
                abort(404)
            category = Category(name=category_name, author_id=user.id)
            db.session.add(category)
            db.session.commit()
            flash('Add a new album successfully!')
            return redirect(url_for('gallery.upload'))
        else:
            flash("Hey! Don't forget put a name for your category!")
            return redirect(url_for('.create_album'))
    return render_template('gallery/create_album.html', form=form)


@gallery.route('/upload', methods=['GET', 'POST'])
def upload():
    form = ImageForm()
    if request.method == 'POST':
        if form.image.data.filename and form.category.data:
            filename = secure_filename(form.image.data.filename)
            user = User.query.filter_by(username=current_user.username).first_or_404()
            if user is None:
                abort(404)

            personal_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user.id))
            if not os.path.exists(personal_dir):
                os.mkdir(personal_dir)

            album_path = os.path.join(personal_dir, str(form.category.data.id))
            if not os.path.exists(album_path):
                os.mkdir(album_path)

            if form.name.data:
                filename = form.name.data
            # image_url = os.path.join(album_path, filename)
            # form.image.data.save(image_url)
            image = Image(category=str(form.category.data), category_id=form.category.data.id)
            db.session.add(image)
            db.session.commit()
            image_id = str(image.id)
            image_path = os.path.join(album_path, image_id)
            form.image.data.save(image_path)
            cat = Category.query.filter_by(id=form.category.data.id).first()
            cat.add_one(image_id)  # Update the album counter by call instance method!
            db.session.add(cat)

            flash('Upload image successfully!')
            return redirect(url_for('gallery.index'))
        else:
            flash('Please choose one image and pick one category before you upload!')
            return redirect(url_for('.upload'))

    return render_template('gallery/upload.html', form=form)


@gallery.route('/lists/<category_id>')
def lists(category_id):
    album = Category.query.filter_by(id=category_id).first()
    images = album.images.order_by(Image.timestamp.desc())
    return render_template('gallery/lists.html', images=images)


@gallery.route('/heads/<category_id>/<image_id>')
def send_image(category_id, image_id):
    # personal_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], category)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    if user is None:
        abort(404)
    if category_id == 'tmp':
        personal_dir = current_app.config['EXTRACT_FOLDER'] + '/'
    else:
        personal_dir = current_app.config['UPLOAD_FOLDER'] + '/' + str(user.id) + '/' + category_id + '/'
    return send_from_directory(personal_dir, image_id)


@gallery.route('/editting/<category_id>/<image_id>')
def single_image(category_id, image_id):
    # personal_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], category)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    if user is None:
        abort(404)
    personal_dir = current_app.config['UPLOAD_FOLDER'] + '/' + str(user.id) + '/' + category_id + '/'
    return send_from_directory(personal_dir, image_id)


@gallery.route('/swa/<category_id>/<image_id>', methods=['GET', 'POST'])
def switch_algorithm(category_id, image_id):
    form = SwitchAlgorithmForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            endpoint = '.' + str(form.type.data)
            return redirect(url_for(endpoint, category_id=category_id, image_id=image_id))
    return render_template('gallery/switch_algorithm.html', category_id=category_id, image_id=image_id, form=form)


@gallery.route('/vs/<category_id>/<image_id>', methods=['GET', 'POST'])
def visible_mark(category_id, image_id):
    return render_template('gallery/area_select.html', category_id=category_id, image_id=image_id)


@gallery.route('/ivs/<category_id>/<image_id>', methods=['GET', 'POST'])
def invisible_mark(category_id, image_id):
    form = InvisibleForm()
    if request.method == "POST":
        if form.validate_on_submit():
            #: You celery load the image here~
            user = User.query.filter_by(username=current_user.username).first_or_404()
            if user is None:
                abort(404)
        personal_dir = current_app.config['UPLOAD_FOLDER'] + '/' + str(user.id) + '/' + category_id + '/'
        image_path = personal_dir + image_id
        watermark_context = form.text.data
        watermark_password = form.password.data
        suffix = current_app.config.get('MARK', '')
        # celery.send_task("tasks.embed_string",
        #                  [image_path, image_id, suffix, watermark_context, watermark_password])
        flash('You have process on the background!')
        return redirect(url_for('.lists', category_id=category_id))

    return render_template('gallery/invisible.html', category_id=category_id, image_id=image_id, form=form)


@gallery.route('/pvs/<category_id>/<image_id>', methods=['GET', 'POST'])
def print_watermark(category_id, image_id):
    return render_template('gallery/area_select.html', category_id=category_id, image_id=image_id)


@gallery.route('/extract', methods=['GET', 'POST'])
def extract():
    form = ExtractForm()
    if request.method == 'POST':
        image = Extract()
        db.session.add(image)
        db.session.commit()
        image_id = str(image.id)
        tmp_path = current_app.config['EXTRACT_FOLDER']
        image_path = os.path.join(tmp_path, image_id)
        if not os.path.exists(tmp_path):
            os.mkdir(tmp_path)
        form.image.data.save(image_path)
        # TODO call extract by celery
        flash('You task had send to celery! you will redirect to a result page!')
        return redirect(url_for('.result', image_id=image_id))
    else:
        flash('Please upload your target image!')
    return render_template('gallery/extract.html', form=form)


@gallery.route('/', methods=['GET', 'POST'])
@gallery.route('/downloads', methods=['GET', 'POST'])
def downloads():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    if user is None:
        abort(404)
    # albums = Category.query.filter_by(author_id=user.id).all()
    albums = Category.query.filter_by(author_id=user.id).all()
    watermark_albums = []
    for album in albums:
        if album.watermark_count == 0:
            # Because there are no more than one image have watermark!!
            # album = []  # empty the no-useful query result!
            pass
        else:
            # album = Category.query.filter_by(author_id=user.id)
            watermark_albums.append(album)
    size_album = len(watermark_albums)
    return render_template('gallery/downloads.html', size_album=size_album, albums=watermark_albums)


@gallery.route('/downloads/<category_id>')
def download(category_id):
    album = Category.query.filter_by(id=category_id).first()
    images = album.images.order_by(Image.timestamp.desc())
    return render_template('gallery/download.html', images=images)


@gallery.route('/downloading/<category_id>/<image_id>', methods=['GET', 'POST'])
def downloading(category_id, image_id):
    personal_dir = current_app.config['UPLOAD_FOLDER'] + '/' + str(current_user.id)
    image_path = personal_dir + '/' + str(category_id)
    suffix = current_app.config.get('MARK', '')
    return send_from_directory(image_path, suffix + str(image_id), as_attachment=True)


@gallery.route('/result/<image_id>')
def result(image_id):
    image = Extract.query.filter_by(id=image_id).first()
    if image:
        flash('Extract done!')
        watermark_context = image.watermark
        watermark_context = 'something'
        if watermark_context:
            flash('The target image have mark with watermark!')
            return render_template('gallery/show_result.html', image_id=image_id, watermark_context=watermark_context)
        else:
            flash('The target image can\'t extract any watermark!')
            return redirect(url_for('.extract'))
    else:
        flash('Please try again later!!')
    return render_template('gallery/show_result.html')
