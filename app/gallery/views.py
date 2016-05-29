import os
import time
from flask import Blueprint, render_template, request, current_app, send_from_directory, \
    redirect, url_for, flash, abort
from flask.ext.login import login_user, login_required, current_user
from werkzeug import secure_filename
from ..models import User, Image, Category
from . import gallery
from .forms import ImageForm
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
    c = Category.query.filter_by(author_id=user.id).first()

    if c is None:
        return redirect(url_for('.create_album'))
    return render_template('gallery/index.html')


@gallery.route('/cm')
def create_album():
    flash('You have to create a album!')
    return render_template('gallery/create_album.html')


@login_required
@gallery.route('/upload', methods=['GET', 'POST'])
def upload():
    form = ImageForm()
    if request.method == 'POST':
        if form.image.data.filename:
            filename = secure_filename(form.image.data.filename)
            personal_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], str(current_user.id))
            print '....', personal_dir
            if not os.path.exists(personal_dir):
                print 'can i come to here'
                try:
                    os.mkdir(personal_dir)
                except IOError, e:
                    print 'Make dir failure ', e
            image_url = os.path.join(personal_dir, filename)
            form.image.data.save(image_url)
            image = Image(url=filename, author=current_user._get_current_object())
            # gen_thumbnail(filename)#TODO celery client will do it ...
            db.session.add(image)
            db.session.commit()
            flash('You have add a new photo!')
            return redirect(url_for('.index'))
        else:
            flash('You should choose a image to input')
            return redirect(url_for('.upload'))
    else:
        filename = None

    return render_template('gallery/upload.html', form=form)
