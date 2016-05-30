import os
import time
from flask import Blueprint, render_template, request, current_app, send_from_directory, \
    redirect, url_for, flash, abort
from flask.ext.login import login_user, login_required, current_user
from werkzeug import secure_filename
from ..models import User, Image, Category
from . import gallery
from .forms import ImageForm, CategoryForm, ImageEdit
from app import db


@gallery.route('/', methods=['GET', 'POST'])
@gallery.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    if user is None:
        abort(404)

    # pagination = user.image.order_by(Image.timestamp.desc()).paginate(
    #         page, per_page=current_app.config['LANDPACK_IMAGE_PER_PAGE'],
    #         error_out=False
    # )
    # posts = pagination.items
    # return render_template('gallery/index.html', posts=posts, pagination=pagination)
    albums = Category.query.filter_by(author_id=user.id).all()
    if len(albums) == 0:
        flash('You have to create a album!')
        return redirect(url_for('.create_album'))

    # image = albums[0].images.order_by(Image.timestamp.desc()).first()
    images = []
    for album in albums:
        Image.query.filter_by(category_id=album.id).first()

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

            return redirect(url_for('.add_category'))
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

            image_url = os.path.join(album_path, filename)
            form.image.data.save(image_url)
            image = Image(name=form.name.data, category=str(form.category.data), url=image_url, filename=filename,
                          category_id=form.category.data.id)

            cat = Category.query.filter_by(id=form.category.data.id).first()
            cat.add_one(filename)  # Update the album counter by call instance method!
            db.session.add(cat)
            db.session.add(image)
            db.session.commit()
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


@gallery.route('/heads/<category>/<filename>')
def send_image(category, filename):
    # personal_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], category)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    if user is None:
        abort(404)
    personal_dir = current_app.config['UPLOAD_FOLDER'] + '/' + str(user.id) + '/' + category + '/'
    return send_from_directory(personal_dir, filename)





@gallery.route('/editting/<category>/<filename>')
def single_image(category, filename):
    # personal_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], category)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    if user is None:
        abort(404)
    personal_dir = current_app.config['UPLOAD_FOLDER'] + '/' + str(user.id) + '/' + category + '/'
    return send_from_directory(personal_dir, filename)


@gallery.route('/edit/<category>/<filename>')
def edit(category, filename):
    form = ImageEdit()
    if form.validate_on_submit():
        print form.x1.data
    return render_template('gallery/image_edit.html', category=category, filename=filename, form=form)
