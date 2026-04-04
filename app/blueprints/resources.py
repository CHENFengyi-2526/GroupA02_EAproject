# app/blueprints/resources.py
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user
from app.decorators import admin_required
from app.extensions import db
from app.models.resource import Resource, ResourceCategory, ResourceTag, ResourceDownload, resource_tag_association
from app.forms import ResourceForm, ResourceTagForm
from datetime import datetime

bp = Blueprint('resources', __name__, url_prefix='/resources')

@bp.route('/')
def list():
    category_slug = request.args.get('category')
    if category_slug:
        category = ResourceCategory.query.filter_by(slug=category_slug).first_or_404()
        resources = Resource.query.filter_by(category_id=category.id).all()
    else:
        resources = Resource.query.all()
    categories = ResourceCategory.query.all()
    return render_template('resources/list.html', resources=resources, categories=categories)

@bp.route('/<int:id>')
def view(id):
    resource = Resource.query.get_or_404(id)
    
    return render_template('resources/view.html', resource=resource)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    form = ResourceForm()
    if form.validate_on_submit():
        resource = Resource(
            title=form.title.data,
            description=form.description.data,
            type=form.type.data,
            download_url=form.download_url.data,
            external_link=form.external_link.data,
            file_size=form.file_size.data,
            is_featured=form.is_featured.data,
            category_id=form.category_id.data
        )
        db.session.add(resource)
        db.session.flush()  
       
        tag_names = [t.strip() for t in form.tags.data.split(',') if t.strip()]
        for tag_name in tag_names:
            slug = tag_name.lower().replace(' ', '-')
            tag = ResourceTag.query.filter_by(slug=slug).first()
            if not tag:
                tag = ResourceTag(name=tag_name, slug=slug)
                db.session.add(tag)
            resource.tags.append(tag)
        db.session.commit()
        flash('Resource added', 'success')
        return redirect(url_for('resources.list'))
    return render_template('resources/form.html', form=form)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    resource = Resource.query.get_or_404(id)
    form = ResourceForm(obj=resource)
    
    if request.method == 'GET':
        form.tags.data = ','.join([tag.name for tag in resource.tags])
    if form.validate_on_submit():
        resource.title = form.title.data
        resource.description = form.description.data
        resource.type = form.type.data
        resource.download_url = form.download_url.data
        resource.external_link = form.external_link.data
        resource.file_size = form.file_size.data
        resource.is_featured = form.is_featured.data
        resource.category_id = form.category_id.data
        
        resource.tags.clear()
        tag_names = [t.strip() for t in form.tags.data.split(',') if t.strip()]
        for tag_name in tag_names:
            slug = tag_name.lower().replace(' ', '-')
            tag = ResourceTag.query.filter_by(slug=slug).first()
            if not tag:
                tag = ResourceTag(name=tag_name, slug=slug)
                db.session.add(tag)
            resource.tags.append(tag)
        db.session.commit()
        flash('Resource updated', 'success')
        return redirect(url_for('resources.view', id=resource.id))
    return render_template('resources/form.html', form=form, resource=resource)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete(id):
    resource = Resource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    flash('Resource deleted', 'success')
    return redirect(url_for('resources.list'))


@bp.route('/tags')
def list_tags():
    tags = ResourceTag.query.all()
    return render_template('resources/tags.html', tags=tags)

@bp.route('/tag/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_tag():
    form = ResourceTagForm()
    if form.validate_on_submit():
        tag = ResourceTag(name=form.name.data, slug=form.slug.data)
        db.session.add(tag)
        db.session.commit()
        flash('Tag created', 'success')
        return redirect(url_for('resources.list_tags'))
    return render_template('resources/tag_form.html', form=form)

@bp.route('/tag/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_tag(id):
    tag = ResourceTag.query.get_or_404(id)
    form = ResourceTagForm(obj=tag)
    if form.validate_on_submit():
        tag.name = form.name.data
        tag.slug = form.slug.data
        db.session.commit()
        flash('Tag updated', 'success')
        return redirect(url_for('resources.list_tags'))
    return render_template('resources/tag_form.html', form=form, tag=tag)

@bp.route('/tag/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_tag(id):
    tag = ResourceTag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag deleted', 'success')
    return redirect(url_for('resources.list_tags'))


@bp.route('/<int:id>/download')
@login_required
def download(id):
    resource = Resource.query.get_or_404(id)
    
    download = ResourceDownload(
        user_id=current_user.id,
        resource_id=resource.id,
        ip_address=request.remote_addr
    )
    resource.download_count += 1
    db.session.add(download)
    db.session.commit()
    
    if resource.download_url:
        return redirect(resource.download_url)
    else:
        flash('There is currently no direct download link for this resource.', 'warning')
        return redirect(url_for('resources.view', id=resource.id))

@bp.route('/my-downloads')
@login_required
def my_downloads():
    downloads = ResourceDownload.query.filter_by(user_id=current_user.id).order_by(ResourceDownload.downloaded_at.desc()).all()
    return render_template('resources/my_downloads.html', downloads=downloads)