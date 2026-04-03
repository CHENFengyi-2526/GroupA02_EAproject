from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models.resource import Resource, Category, ResourceTag
from app.forms import ResourceForm

bp = Blueprint('resources', __name__, url_prefix='/resources')


def process_tags(tag_string, resource):


    ResourceTag.query.filter_by(resource_id=resource.id).delete()
    if tag_string:
        tags = [t.strip() for t in tag_string.split(',') if t.strip()]
        for tag_name in tags:
            tag = ResourceTag(tag_name=tag_name, resource_id=resource.id)
            db.session.add(tag)


@bp.route('/')
def list_resources():

    resources = Resource.query.order_by(Resource.created_at.desc()).all()
    categories = Category.query.all()
    return render_template('resources/list.html', resources=resources, categories=categories)

@bp.route('/category/<int:category_id>')
def list_by_category(category_id):

    category = Category.query.get_or_404(category_id)
    resources = Resource.query.filter_by(category_id=category_id).all()
    return render_template('resources/list.html', resources=resources, category=category)

@bp.route('/<int:id>')
def view_resource(id):

    resource = Resource.query.get_or_404(id)
    return render_template('resources/detail.html', resource=resource)


@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_resource():

    form = ResourceForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        resource = Resource(
            title=form.title.data,
            description=form.description.data,
            file_url=form.file_url.data,
            user_id=current_user.id,
            category_id=form.category_id.data
        )
        db.session.add(resource)
        db.session.commit()

        process_tags(form.tags.data, resource)
        db.session.commit()
        flash('Resource uploaded successfully.', 'success')
        return redirect(url_for('resources.view_resource', id=resource.id))
    return render_template('resources/upload.html', form=form, edit=False)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_resource(id):
    #Edit
    resource = Resource.query.get_or_404(id)
    if resource.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    form = ResourceForm(obj=resource)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    if request.method == 'GET':
        tags = ','.join([t.tag_name for t in resource.tags])
        form.tags.data = tags
    if form.validate_on_submit():
        resource.title = form.title.data
        resource.description = form.description.data
        resource.file_url = form.file_url.data
        resource.category_id = form.category_id.data
        db.session.commit()
        process_tags(form.tags.data, resource)
        db.session.commit()
        flash('Resource updated.', 'success')
        return redirect(url_for('resources.view_resource', id=resource.id))
    return render_template('resources/upload.html', form=form, edit=True)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_resource(id):
    #delete
    resource = Resource.query.get_or_404(id)
    if resource.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    db.session.delete(resource)
    db.session.commit()
    flash('Resource deleted.', 'success')
    return redirect(url_for('resources.list_resources'))